import boto3
import argparse
import os


def sync_directory_to_s3(local_path, bucket_name, s3_path, s3_client):
    for subdir, _, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(subdir, file)
            s3_file_path = os.path.join(
                s3_path, os.path.relpath(local_file_path, local_path)
            )
            s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
            print(
                f"Uploaded {local_file_path} to {s3_file_path} in bucket {bucket_name}."
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync local directory to S3.")
    parser.add_argument(
        "--local_path", type=str, required=True, help="Local directory path to sync"
    )
    parser.add_argument(
        "--bucket_name", type=str, required=True, help="Name of the S3 bucket"
    )
    parser.add_argument(
        "--s3_path", type=str, required=True, help="S3 directory path to sync to"
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

    sync_directory_to_s3(args.local_path, args.bucket_name, args.s3_path, s3_client)
