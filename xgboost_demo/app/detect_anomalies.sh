#!/bin/bash

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Load settings from settings.conf
source settings.conf

# Check if required parameters are set
if [ -z "$MODEL_PATH" ] || [ -z "$PRODUCTION_DATA_PATH" ] || [ -z "$OUTPUT_DIR" ]; then
    handle_error "Missing settings. Make sure MODEL_PATH, PRODUCTION_DATA_PATH, and OUTPUT_DIR are set in settings.conf"
fi

# Run the Python script to classify instances in synthetic production data
python detect_anomalies.py --model_path $MODEL_PATH --production_data_path $PRODUCTION_DATA_PATH --output_dir $OUTPUT_DIR

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "Classification completed successfully."
