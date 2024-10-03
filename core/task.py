from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
import csv
import os
from django.conf import settings
import logging
from django.db import transaction

logger = logging.getLogger('core.task')

@shared_task
def update_pujo_scores():
    logger.info("Pujo Cron Job started")
    from pujo.models import Pujo, LastScoreModel

    current_time = timezone.now()
    X = 3  # Adjust this to the desired number of hours

    pujos = Pujo.objects.filter(updated_at__lt=current_time - timezone.timedelta(hours=X))
    if not pujos.exists():
        logger.info("No pujos found for score update.")
    else:
        for pujo in pujos:
            # Sum all positive last scores in the last 2X hours
            last_scores = LastScoreModel.objects.filter(
                pujo=pujo,
                last_updated_at__gt=current_time - timezone.timedelta(hours=2 * X)
            )

            # Sum all positive scores
            score_sum = sum(score.value for score in last_scores if score.value > 0)

            # Update the pujo's score
            pujo.search_score = max(pujo.search_score - score_sum, 0)

            # Use a transaction to ensure data integrity
            with transaction.atomic():
                pujo.save()
                # Remove all previous last scores using bulk_delete if applicable
                last_scores.delete()  
                LastScoreModel.objects.create(pujo=pujo, value=-score_sum)

    logger.info("Pujo Cron Job Ended")


@shared_task
def backup_logs_to_minio():
    logger.info("Started backing up the log files")
    
    # Initialize MinIO client
    try:
        minio_client = initialize_minio_client()
    except Exception as e:
        logger.error(f"Failed to initialize MinIO client: {str(e)}")
        return

    # Directory to save CSV files
    local_backup_dir = settings.MEDIA_ROOT

    # Step 1: Upload any existing local CSV files
    upload_existing_csv_files(minio_client, local_backup_dir)

    # Step 2: Create a new CSV file with logs older than 20 minutes and upload it
    create_and_upload_log_backup(minio_client, local_backup_dir)


def initialize_minio_client():
    """Initialize and return a MinIO client."""
    from minio import Minio

    return Minio(
        settings.MINIO_URL,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=True  # This is set to True because of the https URL
    )


def upload_existing_csv_files(minio_client, local_backup_dir):
    """Check and upload any existing CSV files in the backup directory to MinIO."""
    for file in os.listdir(local_backup_dir):
        if file.endswith("_logs.csv"):
            file_path = os.path.join(local_backup_dir, file)
            try:
                logger.info(f"Found an existing CSV file to backup: {file}")
                upload_file_to_minio(minio_client, file, file_path)
                verify_and_delete_local_file(minio_client, file, file_path)
            except Exception as e:
                logger.error(f"Failed to upload file {file} to MinIO: {str(e)}")


def create_and_upload_log_backup(minio_client, local_backup_dir):
    """Create a new CSV file with logs older than 20 minutes and upload it to MinIO."""
    from Log.models import Log
    filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + "_logs.csv"
    file_path = os.path.join(local_backup_dir, filename)

    # Calculate the time buffer (20 minutes)
    buffer_time = timezone.now() - timedelta(minutes=20)

    # Fetch logs created more than 20 minutes ago
    logs = Log.objects.filter(created_at__lt=buffer_time)

    # Create a CSV file and write log data
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'level', 'message', 'module', 'user_id', 'created_at'])  # Write headers
        for log in logs:  # Write data rows
            writer.writerow([log.id, log.level, log.message, log.module, log.user_id, log.created_at])

    # Upload the newly created CSV file to MinIO
    try:
        upload_file_to_minio(minio_client, filename, file_path)
        verify_and_delete_local_file(minio_client, filename, file_path)
        # Delete logs from the database if backup is successful
        logs.delete()
        logger.info("Logs older than 20 minutes successfully deleted from the database.")
    except Exception as e:
        logger.error(f"Failed to upload file {filename} to MinIO: {str(e)}")


def upload_file_to_minio(minio_client, filename, file_path):
    """Upload a file to MinIO bucket."""
    if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
        minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

    minio_client.fput_object(
        settings.MINIO_BUCKET_NAME,
        filename,
        file_path,
        content_type='application/csv'
    )
    logger.info(f"File {filename} uploaded to MinIO bucket {settings.MINIO_BUCKET_NAME} successfully.")


def verify_and_delete_local_file(minio_client, filename, file_path):
    """Verify if the file is in MinIO and delete the local copy if successful."""
    objects = minio_client.list_objects(settings.MINIO_BUCKET_NAME, prefix=filename)
    file_found = any(obj.object_name == filename for obj in objects)

    if file_found:
        logger.info(f"File {filename} verified in MinIO bucket {settings.MINIO_BUCKET_NAME}.")
        os.remove(file_path)
        logger.info(f"Local file {filename} successfully deleted after backup.")
    else:
        logger.warning(f"Verification failed: File {filename} not found in MinIO bucket {settings.MINIO_BUCKET_NAME}.")
