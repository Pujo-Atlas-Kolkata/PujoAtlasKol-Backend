from celery import shared_task
from django.utils import timezone
from pujo.models import Pujo, LastScoreModel
from django.utils import timezone
import csv
import os
from datetime import datetime
from django.conf import settings
from minio import Minio
from Log.models import Log
from decouple import config


@shared_task
def update_pujo_scores():
    current_time = timezone.now()
    # Adjust X to the desired number of hours
    X = 6  

    pujos = Pujo.objects.filter(updated_at__lt=current_time - timezone.timedelta(hours=X))
    for pujo in pujos:
        # Sum all positive last scores in the last 2X hours
        last_scores = LastScoreModel.objects.filter(
            pujo=pujo,
            last_updated_at__gt=current_time - timezone.timedelta(hours=2 * X),
            value__gt=0
        )

        # sum all positive scores
        score_sum = sum(score.value for score in last_scores if score.value > 0)

        # Update the pujo's score and make sure it does not go belowe zero
        pujo.search_score = max(pujo.search_score - score_sum, 0)
        pujo.save()

        # Remove all previous last scores
        last_scores.delete()

        # Log the score summation - the new score
        LastScoreModel.objects.create(pujo=pujo, value=-score_sum)

# MinIO configuration
# Load environment variables from the .env file

@shared_task
def backup_logs_to_minio():
    print(f"Started backing up the log files")

    # Filename with the current date and time
    filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + "_logs.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Fetch all logs
    logs = Log.objects.all()

    # Create a CSV file and write log data
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow(['id', 'level', 'message', 'module', 'user_id', 'created_at'])
        # Write data rows
        for log in logs:
            writer.writerow([log.id, log.level, log.message, log.module, log.user_id, log.created_at])

    # Initialize MinIO client
    minio_client = Minio(
        settings.MINIO_URL,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=True  # This is set to True because of the https URL
    )

    # Upload the file to MinIO
    try:
        if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
        minio_client.fput_object(
            settings.MINIO_BUCKET_NAME,
            filename,
            file_path,
            content_type='application/csv'
        )
        print(f"File {filename} uploaded to MinIO bucket {settings.MINIO_BUCKET_NAME} successfully.")
        # Verification Step: Check if the file is present in the bucket
        objects = minio_client.list_objects(settings.MINIO_BUCKET_NAME, prefix=filename)
        file_found = any(obj.object_name == filename for obj in objects)

        if file_found:
            print(f"File {filename} verified in MinIO bucket {settings.MINIO_BUCKET_NAME}.")
        else:
            print(f"Verification failed: File {filename} not found in MinIO bucket {settings.MINIO_BUCKET_NAME}.")

    
    except Exception as e:
        print(f"Failed to upload file to MinIO: {str(e)}")
    finally:
        # Delete the CSV file from local after uploading to MinIO
        if os.path.exists(file_path):
            os.remove(file_path)

    # Delete logs from the database that have been backed up
    logs.delete()
