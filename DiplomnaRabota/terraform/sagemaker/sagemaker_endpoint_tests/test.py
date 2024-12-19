import boto3
import pickle
import pandas as pd
from io import BytesIO

# Create a session using your AWS credentials
s3_client = boto3.client('s3')

# Specify your bucket name and the key (file path) of your ARIMA model
bucket_name = 'arima-model'
model_key = 'arima_model.pkl'

# Fetch the model file from S3
response = s3_client.get_object(Bucket=bucket_name, Key=model_key)
model_data = response['Body'].read()

# Load the model using pickle from the in-memory data
model = pickle.load(BytesIO(model_data))

# Create some sample test data (must have a similar format to training data)
timestamp = pd.date_range(start="2025-01-01", periods=1, freq='D')
value = 0.544321
input_df = pd.DataFrame({'timestamp': timestamp, 'value': value})

# Perform prediction using the 'predict' method
forecast = model.predict(start=len(input_df), end=len(input_df))
print(forecast)
