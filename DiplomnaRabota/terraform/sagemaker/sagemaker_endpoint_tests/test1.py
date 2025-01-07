import boto3
import json

# Configure SageMaker client
region = "eu-central-1"
endpoint_name = "ppetrov-endpoint"
runtime_client = boto3.client("sagemaker-runtime", region_name=region)

# Define input data
input_data = {}  # Replace with your input

# Invoke the endpoint
response = runtime_client.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=json.dumps(input_data),
    ContentType="application/json"
)

# Decode and print the prediction
result = json.loads(response["Body"].read().decode())
print("Prediction:", result)
