#!/bin/bash

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Load settings from settings.conf
source settings.conf

# Check if required parameters are set
if [ -z "$LOCAL_PATH" ] || [ -z "$BUCKET_NAME" ] || [ -z "$S3_PATH" ] || [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    handle_error "Missing settings. Make sure all necessary parameters are set in settings.conf"
fi

# Run the Python script to sync S3 directory to local directory
python sync_from_s3.py --local_path $LOCAL_PATH --bucket_name $BUCKET_NAME --s3_path $S3_PATH --aws_access_key_id $AWS_ACCESS_KEY_ID --aws_secret_access_key $AWS_SECRET_ACCESS_KEY

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "S3 directory synced to local directory successfully."
