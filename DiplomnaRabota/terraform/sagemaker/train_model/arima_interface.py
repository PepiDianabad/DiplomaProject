import pickle
import boto3
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from io import BytesIO

def model_fn(model_dir):
    """Load the trained model from S3"""
    s3 = boto3.client('s3')
    
    # Split the S3 path into bucket name and object key
    bucket_name = model_dir.split('/')[0]  # e.g., 'my-bucket'
    object_key = '/'.join(model_dir.split('/')[1:]) + 'arima_model.pkl'  # e.g., 'path/to/model/arima_model.pkl'

    model_buffer = BytesIO()

    # Download the model from S3 to the buffer
    s3.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=model_buffer)

    model_buffer.seek(0)  # Move the pointer to the start of the buffer
    model = pickle.load(model_buffer)
    
    return model


def predict_fn(input_data, model):
    """Perform prediction using the loaded ARIMA model"""
    # Assuming input_data is a pandas DataFrame with 'timestamp' and 'value' columns
    input_df = pd.DataFrame(input_data, columns=["timestamp", "value"])
    input_df["timestamp"] = pd.to_datetime(input_df["timestamp"])  # Ensure timestamps are datetime objects
    input_df.set_index("timestamp", inplace=True)  # Set timestamp as index for ARIMA
    
    # Forecast using ARIMA model
    forecast = model.forecast(steps=len(input_df))
    return forecast.tolist()

# Example data formatted for input
input_data = [
    ["2024-12-13T13:48:35Z", 0.039049],
    ["2024-12-13T13:48:35Z", 0.350777],
    ["2024-12-13T13:48:35Z", 0.039665],
    ["2024-12-13T13:49:44Z", 0.036023],
    ["2024-12-13T13:49:44Z", 0.347820],
    ["2024-12-13T13:50:44Z", 0.042457],
    ["2024-12-13T13:50:44Z", 0.349761],
    ["2024-12-13T13:51:44Z", 0.041913],
    ["2024-12-13T13:51:44Z", 0.350042],
    ["2024-12-13T13:52:44Z", 0.039783],
    ["2024-12-13T13:52:44Z", 0.350572],
    ["2024-12-13T13:53:44Z", 0.038091],
    ["2024-12-13T13:53:44Z", 0.351294],
    ["2024-12-13T13:54:44Z", 0.037315],
    ["2024-12-13T13:54:44Z", 0.350671],
    ["2024-12-13T13:55:44Z", 0.036909],
    ["2024-12-13T13:55:44Z", 0.352051],
    ["2024-12-13T13:56:44Z", 0.038262],
    ["2024-12-13T13:56:44Z", 0.351889],
    ["2024-12-13T13:57:44Z", 0.039129],
    ["2024-12-13T13:57:44Z", 0.352335],
    ["2024-12-13T13:58:44Z", 0.037776],
    ["2024-12-13T13:58:44Z", 0.352461],
    ["2024-12-13T13:59:44Z", 0.036948],
    ["2024-12-13T13:59:44Z", 0.351775],
    ["2024-12-13T14:00:44Z", 0.038525],
    ["2024-12-13T14:00:44Z", 0.351147],
    ["2024-12-13T14:01:44Z", 0.039089],
    ["2024-12-13T14:01:44Z", 0.352005],
    ["2024-12-13T14:02:44Z", 0.037462],
    ["2024-12-13T14:02:44Z", 0.352169],
    ["2024-12-13T14:03:44Z", 0.036725],
    ["2024-12-13T14:03:44Z", 0.351551],
    ["2024-12-13T14:04:44Z", 0.037992],
    ["2024-12-13T14:04:44Z", 0.352308],
    ["2024-12-13T14:05:44Z", 0.039450],
    ["2024-12-13T14:05:44Z", 0.350934],
    ["2024-12-13T14:06:44Z", 0.040372],
    ["2024-12-13T14:06:44Z", 0.351268],
    ["2024-12-13T14:07:44Z", 0.039726],
    ["2024-12-13T14:07:44Z", 0.351613],
    ["2024-12-13T14:08:44Z", 0.038914],
    ["2024-12-13T14:08:44Z", 0.350899],
    ["2024-12-13T14:09:44Z", 0.037451],
    ["2024-12-13T14:09:44Z", 0.352488],
    ["2024-12-13T14:10:44Z", 0.036823],
    ["2024-12-13T14:10:44Z", 0.352036],
    ["2024-12-13T14:11:44Z", 0.039064],
    ["2024-12-13T14:11:44Z", 0.350158],
    ["2024-12-13T14:12:44Z", 0.038011],
    ["2024-12-13T14:12:44Z", 0.352413],
]


# Load the ARIMA model
model = model_fn('arima-model')

# Make a prediction
forecast = predict_fn(input_data, model)

# Print the forecast result
print(forecast)
