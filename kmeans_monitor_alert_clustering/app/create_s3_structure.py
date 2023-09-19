import boto3
import argparse


def create_s3_structure(bucket_name, paths, prefix, s3_client):
    # Prefixing paths
    prefixed_paths = [f"{prefix}/{path}" for path in paths]

    for path in prefixed_paths:
        s3_client.put_object(Bucket=bucket_name, Key=path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create directory structure in S3.")
    parser.add_argument(
        "--bucket_name", type=str, required=True, help="Name of the S3 bucket"
    )
    parser.add_argument(
        "--paths",
        type=str,
        nargs="+",
        required=True,
        help="List of paths to create in S3",
    )
    parser.add_argument(
        "--prefix", type=str, default="", help="Prefix to prepend to each path"
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

    create_s3_structure(args.bucket_name, args.paths, args.prefix, s3_client)
