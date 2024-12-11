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
            
            # Log the received data
            logger.info(f"Data: {response_json}")
            
            # Save to S3
            save_to_s3(response_json)
            
            return {"message": "Data successfully saved to S3", "data": response_json}
        else:
            logger.error(f"Error response from Prometheus: {response.text}")
            return {"error": "Failed to query Prometheus", "details": response.text}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e

def save_to_s3(data):
    try:
        # Define the S3 bucket name and file key
        bucket_name = "ppetrov-prometheus-metrics-s3"
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        file_key = f"metrics/prometheus_response_{timestamp}.json"
        
        # Convert the data to a JSON string
        json_data = json.dumps(data)
        
        # Upload to S3
        logger.info(f"Saving data to S3 bucket '{bucket_name}' with key '{file_key}'")
        s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=json_data)
        
        logger.info("Data successfully saved to S3.")
    except Exception as e:
        logger.error(f"Failed to save data to S3: {str(e)}")
        raise e
