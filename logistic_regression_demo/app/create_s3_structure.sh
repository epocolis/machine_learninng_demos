#!/bin/bash

# Usage: ./create_s3_structure.sh

# Load settings from settings.conf
source settings.conf

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Check for minimum required settings
if [ -z "$BUCKET_NAME" ] || [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$TRAIN_DIR" ] || [ -z "$VALIDATION_DIR" ] || [ -z "$CONFIG_DIR" ] || [ -z "$MODEL_DIR" ] || [ -z "$OUTPUT_DIR" ]; then
    handle_error "Missing settings. Make sure all necessary parameters are set in settings.conf"
fi

# Parse directory paths into an array for S3
IFS="," read -ra S3_PATHS_ARR <<< "$TRAIN_DIR,$VALIDATION_DIR,$CONFIG_DIR,$MODEL_DIR,$OUTPUT_DIR"

# Run the Python script to create directory structure in S3
python create_s3_structure.py --bucket_name "$BUCKET_NAME" --aws_access_key_id "$AWS_ACCESS_KEY_ID" --aws_secret_access_key "$AWS_SECRET_ACCESS_KEY" --paths "${S3_PATHS_ARR[@]}" --prefix "$PREFIX"

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script for S3 failed"
fi

# Print completion message
echo "S3 directory structure created successfully."
