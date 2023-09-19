import boto3
import argparse
import os


def sync_s3_to_directory(bucket_name, s3_path, local_path, s3_client):
    # List all objects under the specified S3 path
    s3_objects = s3_client.list_objects(Bucket=bucket_name, Prefix=s3_path)["Contents"]

    for s3_object in s3_objects:
        s3_file_path = s3_object["Key"]
        local_file_path = os.path.join(
            local_path, os.path.relpath(s3_file_path, s3_path)
        )

        # Create local directory if it does not exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Download file from S3 to local directory
        s3_client.download_file(bucket_name, s3_file_path, local_file_path)
        print(
            f"Downloaded {s3_file_path} from bucket {bucket_name} to {local_file_path}."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync S3 directory to local directory."
    )
    parser.add_argument(
        "--local_path", type=str, required=True, help="Local directory path to sync to"
    )
    parser.add_argument(
        "--bucket_name", type=str, required=True, help="Name of the S3 bucket"
    )
    parser.add_argument(
        "--s3_path", type=str, required=True, help="S3 directory path to sync from"
    )
    parser.add_argument(
        "--aws_access_key_id", type=str, required=True, help="AWS Access Key ID"
    )
    parser.add_argument(
        "--aws_secret_access_key", type=str, required=True, help="AWS Secret Access Key"
    )

    args = parser.parse_args()

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
    )

    sync_s3_to_directory(args.bucket_name, args.s3_path, args.local_path, s3_client)
