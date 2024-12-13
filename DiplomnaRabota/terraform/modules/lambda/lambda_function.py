import logging
import requests
import boto3
import json
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    logger.info("Starting Lambda Execution...")
    try:
        # Prometheus API endpoint
        prometheus_url = "http://a1bcff183c8064cee907308015e818ce-1619549014.eu-central-1.elb.amazonaws.com:9090/api/v1/query"
        
        # Query for Prometheus
        query = "avg(node_memory_MemFree_bytes / node_memory_MemTotal_bytes) by (instance)"
        
        # Pass query as a parameter
        params = {"query": query}
        
        logger.info(f"Querying Prometheus at {prometheus_url} with query: {query}")
        
        # Perform the HTTP GET request
        response = requests.get(prometheus_url, params=params, timeout=5)
        
        # Log the response status
        logger.info(f"Response from Prometheus: {response.status_code}")
        
        if response.status_code == 200:
            # Parse the JSON response
            response_json = response.json()
            
            # Transform and append the new data to the S3 file
            append_to_s3(response_json)
            
            return {"message": "Data successfully appended to S3 file"}
        else:
            logger.error(f"Error response from Prometheus: {response.text}")
            return {"error": "Failed to query Prometheus", "details": response.text}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e

def append_to_s3(prometheus_data):
    try:
        # Define the S3 bucket name and file key
        bucket_name = "ppetrov-prometheus-metrics-s3"
        file_key = "metrics/deepar_data.jsonl"  # Use a JSONL (JSON Lines) format

        # Transform Prometheus data to DeepAR format
        transformed_data = transform_to_deepar(prometheus_data)

        # Read the existing file from S3 if it exists
        try:
            logger.info(f"Fetching existing file from S3: {file_key}")
            existing_object = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            existing_content = existing_object["Body"].read().decode("utf-8")
        except s3_client.exceptions.NoSuchKey:
            logger.info(f"No existing file found. A new file will be created.")
            existing_content = ""

        # Append the new transformed data to the existing content
        updated_content = existing_content + transformed_data

        # Upload the updated content back to S3
        logger.info(f"Updating file in S3 bucket '{bucket_name}' with key '{file_key}'")
        s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=updated_content)

        logger.info("Data successfully appended to S3 file.")
    except Exception as e:
        logger.error(f"Failed to append data to S3: {str(e)}")
        raise e

def transform_to_deepar(prometheus_data):
    try:
        transformed_records = []

        # Parse the Prometheus response and structure data for DeepAR
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        for result in prometheus_data["data"]["data"]["result"]:
            instance = result["metric"]["instance"]
            value = float(result["value"][1])

            # Create or append to a time series for the instance
            transformed_records.append({
                "start": timestamp,  # The start timestamp for the series
                "target": [value],  # Add this value as part of the target array
                "instance": instance
            })

        # Convert the transformed records to JSONL format
        return "\n".join([json.dumps(record) for record in transformed_records]) + "\n"
    except Exception as e:
        logger.error(f"Failed to transform data: {str(e)}")
        raise e
