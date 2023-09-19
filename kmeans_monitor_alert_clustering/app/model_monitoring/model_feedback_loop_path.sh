#!/bin/bash

# usage: ./feedback_loop.sh opt/ml/model/xgboost_model.model opt/ml/input/data/production/production.csv opt/ml/input/data/production/true_labels.csv opt/ml/monitoring


# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Check if required command-line arguments are provided
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
    handle_error "Missing arguments. Usage: ./feedback_loop.sh <model_path> <production_data_path> <true_labels_path> <output_dir>"
fi

# Command-line arguments
MODEL_PATH=$1
PRODUCTION_DATA_PATH=$2
TRUE_LABELS_PATH=$3
OUTPUT_DIR=$4

# Run the Python script for the feedback loop
python feedback_loop.py --model_path $MODEL_PATH --production_data_path $PRODUCTION_DATA_PATH --true_labels_path $TRUE_LABELS_PATH --output_dir $OUTPUT_DIR

# Check for Python script errors
if [ $? -ne 0 ]; then
    handle_error "Python script failed"
fi

# Print completion message
echo "Feedback loop completed successfully."
