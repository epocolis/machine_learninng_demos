#!/bin/bash

# Load settings from settings.conf
source settings.conf

# Function to print error message and exit
handle_error() {
    echo "Error: $1"
    exit 1
}

# Delete previous directories if they exist
rm -rf $TRAIN_DIR || handle_error "Failed to remove existing train directory"
rm -rf $VALIDATION_DIR || handle_error "Failed to remove existing validation directory"
rm -rf $CONFIG_DIR || handle_error "Failed to remove existing config directory"
rm -rf $MODEL_DIR || handle_error "Failed to remove existing model directory"
rm -rf $OUTPUT_DIR || handle_error "Failed to remove existing output directory"

# Create the directory structure for mimicking SageMaker environment
mkdir -p $TRAIN_DIR || handle_error "Failed to create train directory"
mkdir -p $VALIDATION_DIR || handle_error "Failed to create validation directory"
mkdir -p $CONFIG_DIR || handle_error "Failed to create config directory"
mkdir -p $MODEL_DIR || handle_error "Failed to create model directory"
mkdir -p $OUTPUT_DIR || handle_error "Failed to create output directory"

# Create .empty placeholder files (optional)
touch $TRAIN_DIR/.empty || handle_error "Failed to create .empty in train directory"
touch $VALIDATION_DIR/.empty || handle_error "Failed to create .empty in validation directory"
touch $CONFIG_DIR/.empty || handle_error "Failed to create .empty in config directory"
touch $MODEL_DIR/.empty || handle_error "Failed to create .empty in model directory"
touch $OUTPUT_DIR/.empty || handle_error "Failed to create .empty in output directory"

echo "SageMaker directory structure and .empty placeholder files created successfully."
