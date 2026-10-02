import boto3 

from config import AWS_REGION 

s3 = boto3.client(
    "s3",
    region_name = AWS_REGION
)

def upload_file(file_path,bucket_name,object_key):
    s3.upload_file(
        file_path, 
        bucket_name,
        object_key
    )
    print(f"Uploaded: s3://{bucket_name}/{object_key}")