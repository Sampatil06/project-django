import base64
import boto3
import os
import json

# Initialize the S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Retrieve bucket name from environment variables
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is not set.")
        
        # Retrieve input data from the event
        file_name = event.get('file_name')
        file_content_base64 = event.get('file_content')
        
        if not file_name or not file_content_base64:
            raise ValueError("Both 'file_name' and 'file_content' must be provided in the input.")
        
        # Fix incorrect padding by adding the correct number of '=' characters
        missing_padding = len(file_content_base64) % 4
        if missing_padding:
            file_content_base64 += '=' * (4 - missing_padding)
        
        # Decode the Base64-encoded file content
        file_content = base64.b64decode(file_content_base64)
        
        # Upload the file to the S3 bucket
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File uploaded successfully.',
                'file_name': file_name,
                'bucket_name': bucket_name
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
