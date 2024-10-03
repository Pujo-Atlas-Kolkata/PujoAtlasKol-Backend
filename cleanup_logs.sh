#!/bin/bash

# Define an array of log file paths
log_files=(
    "/var/log/supervisor/celery_worker.log"
    "/var/log/supervisor/celery_worker_err.log"
    "/var/log/supervisor/celery_beat.log"
    "/var/log/supervisor/celery_beat_err.log"
    "/var/log/supervisor/redis.log"
    "/var/log/supervisor/redis_err.log"
    "/var/log/supervisor/django_runserver.log"
    "/var/log/supervisor/django_runserver_err.log"
)

# Loop through each file in the array
for log_file in "${log_files[@]}"; do
    if [ -e "$log_file" ]; then
        echo "Removing: $log_file"
        rm -rf "$log_file"
    else
        echo "File not found: $log_file"
    fi
done

echo "Cleanup complete."
