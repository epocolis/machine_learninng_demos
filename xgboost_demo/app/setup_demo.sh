# create local directory structure
./create_local_file_structure.sh

# create s3 directory structure 
./create_s3_structure.sh

# generate and save synthetic data
./generate_synthetic_data_from_settings.sh

# train model locally on synthetic data 



# upload model,data, metrics to S3, sync local directory with S3