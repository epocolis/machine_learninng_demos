#!/bin/bash

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Load settings from settings.conf
source settings.conf

# Check if required parameters are set
if [ -z "$INPUT_DATA_FILENAME" ] || [ -z "$OUTPUT_FILENAME" ] || [ -z "$OUTPUT_DIR" ]; then
    handle_error "Missing settings. Make sure INPUT_DATA_FILENAME, OUTPUT_FILENAME, and OUTPUT_DIR are set in settings.conf"
fi

# Make sure the directory exists
mkdir -p $OUTPUT_DIR || handle_error "Failed to create or access directory $OUTPUT_DIR"

# Full paths to the input and output files
INPUT_DATA_PATH="$INPUT_DIR/$INPUT_DATA_FILENAME"
OUTPUT_DATA_PATH="$OUTPUT_DIR/$OUTPUT_FILENAME"

# Run the Python script to cluster instances in synthetic monitoring alert data
python perform_clustering.py --input_data_path $INPUT_DATA_PATH --output_dir $OUTPUT_DIR --output_filename $OUTPUT_FILENAME

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "Clustering completed successfully."
