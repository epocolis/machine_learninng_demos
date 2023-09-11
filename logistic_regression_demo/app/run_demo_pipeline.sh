# get model and data from s3
./sync_s3_to_local.sh
# perform classification
./perform_rca_with_logistic_regression.sh
# sync results to s3
./sync_local_to_s3.sh
