./create_s3_structure.sh my_bucket AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY "opt/ml/input/data/train/" "opt/ml/input/data/validation/"

# upload demo data and files up to S3
./sync_from_s3.sh opt/ml/input/data my_bucket xgboost_anomaly_detection/opt/ml/input/data AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY


# download model and data from S3
./sync_from_s3.sh opt/ml/input/data my_bucket xgboost_anomaly_detection/opt/ml/input/data AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY


