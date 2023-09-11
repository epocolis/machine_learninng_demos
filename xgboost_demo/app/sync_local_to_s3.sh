#!/bin/bash

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Check if required command-line arguments are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ]; then
    handle_error "Missing arguments. Usage: ./sync_to_s3.sh <local_path> <bucket_name> <s3_path> <aws_access_key_id> <aws_secret_access_key>"
fi

# Command-line arguments
LOCAL_PATH=$1
BUCKET_NAME=$2
S3_PATH=$3
AWS_ACCESS_KEY_ID=$4
AWS_SECRET_ACCESS_KEY=$5

# Run the Python script to sync local directory to S3
python sync_to_s3.py --local_path $LOCAL_PATH --bucket_name $BUCKET_NAME --s3_path $S3_PATH --aws_access_key_id $AWS_ACCESS_KEY_ID --aws_secret_access_key $AWS_SECRET_ACCESS_KEY

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "Local directory synced to S3 successfully."
