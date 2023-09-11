#!/bin/bash

# Load settings from settings.conf
source settings.conf

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Check for minimum required settings
if [ -z "$TRAIN_FILE" ] || [ -z "$VALIDATION_FILE" ] || [ -z "$OUTPUT_DIR" ] || [ -z "$MODEL_DIR" ] || [ -z "$PARAMS" ]; then
    handle_error "Missing settings. Make sure all necessary parameters are set in settings.conf"
fi

# Create output and model directories if they don't exist
mkdir -p $OUTPUT_DIR || handle_error "Failed to create output directory"
mkdir -p $MODEL_DIR || handle_error "Failed to create model directory"

# Run the Python script to train and evaluate the XGBoost model
python train_xgboost_anomaly_detection.py --train_file $TRAIN_FILE --validation_file $VALIDATION_FILE --output_dir $OUTPUT_DIR --model_dir $MODEL_DIR --params "$PARAMS"

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "Training and evaluation completed successfully."
