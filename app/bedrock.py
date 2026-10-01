import boto3
from config import AWS_REGION, BEDROCK_MODEL_ID, MAX_OUTPUT_TOKENS 

client = boto3.client(
    "bedrock-runtime", 
    region_name="us-east-1"
)

