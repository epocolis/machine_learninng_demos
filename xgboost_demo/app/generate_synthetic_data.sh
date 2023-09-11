#!/bin/bash

# Load settings from settings.conf
source settings.conf

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Check for minimum required settings
if [ -z "$N_SAMPLES" ] || [ -z "$ANOMALY_RATIO" ] || [ -z "$SEED" ] || [ -z "$TRAIN_DIR" ] || [ -z "$VALIDATION_DIR" ] || [ -z "$PRODUCTION_DIR" ]; then
    handle_error "Missing settings. Make sure all necessary parameters are set in settings.conf"
fi

# Create directories if they don't exist
mkdir -p $TRAIN_DIR || handle_error "Failed to create train directory"
mkdir -p $VALIDATION_DIR || handle_error "Failed to create validation directory"
mkdir -p $PRODUCTION_DIR || handle_error "Failed to create production directory"

# Run the Python script to generate synthetic data and save to specified directories
python generate_synthetic_data.py --n_samples $N_SAMPLES --anomaly_ratio $ANOMALY_RATIO --seed $SEED --train_dir $TRAIN_DIR --validation_dir $VALIDATION_DIR --production_dir $PRODUCTION_DIR

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "Synthetic data generated and saved to specified directories."
