import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Define the S3 bucket and object key
    bucket_name = "ppetrov-prometheus-metrics-s3"
    object_key = "metrics_data.json"
    
    # Data you want to save in S3 (this is just an example, adjust according to your use case)
    data = {
        "message": "Lambda function triggered successfully!",
        "event": event
    }
    
    # Save the data to S3
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json.dumps(data),
            ContentType="application/json"
        )
        print(f"Data successfully written to {bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error writing to S3: {e}")
        raise e
