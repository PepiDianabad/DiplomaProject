import boto3
import json

# Create a SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime', region_name='eu-central-1')

# The name of your endpoint
endpoint_name = 'ppetrov-endpoint'

# Sample input data (adjust based on your model input format)
payload = {
    "timestamp": ["2024-01-01 00:00:00", "2024-01-02 00:00:00", "2024-01-03 00:00:00"],
    "value": [0, 0, 0]
}


# Convert the payload to a JSON string
payload_json = json.dumps(payload)

# Invoke the endpoint
response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',  # Ensure the content type matches your model input
    Accept='application/json',  # Response format
    Body=payload_json
)

# Get the result from the response
result = json.loads(response['Body'].read().decode())

print(result)
