#!/bin/bash

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Load settings from settings.conf
source settings.conf

# Check if required parameters are set
if [ -z "$N_SAMPLES" ] || [ -z "$DATA_SYNTHESIS_DIR" ] || [ -z "$SYNTHETIC_DATA_FILENAME" ] || [ -z "$SEED" ]; then
    handle_error "Missing settings. Make sure N_SAMPLES, DATA_SYNTHESIS_DIR, SYNTHETIC_DATA_FILENAME, and SEED are set in settings.conf"
fi

# Make sure the directory exists
mkdir -p $DATA_SYNTHESIS_DIR || handle_error "Failed to create or access directory $DATA_SYNTHESIS_DIR"

# Full paths to the input and output files
SYNTHETIC_DATA_PATH="$DATA_SYNTHESIS_DIR/$SYNTHETIC_DATA_FILENAME"

# Run the Python script to generate synthetic data
python generate_synthetic_data.py --n_samples $N_SAMPLES --seed $SEED --output_dir $DATA_SYNTHESIS_DIR --output_filename $SYNTHETIC_DATA_FILENAME

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "Synthetic data generation completed successfully."
