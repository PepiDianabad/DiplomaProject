import pickle
import boto3
import pandas as pd
from flask import Flask, request, jsonify
from statsmodels.tsa.arima.model import ARIMA
from io import BytesIO, StringIO

# Define S3 bucket and keys for both the model and metrics
model_bucket = "arima-model"
model_key = "arima_model.pkl"
metrics_bucket = "ppetrov-prometheus-metrics-s3"
metrics_key = "metrics/model_data.jsonl"

app = Flask(__name__)

def load_model_from_s3(bucket_name, object_key):
    """Load the trained ARIMA model from S3."""
    s3 = boto3.client('s3')
    model_buffer = BytesIO()
    try:
        s3.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=model_buffer)
        print(f"Model successfully downloaded from s3://{bucket_name}/{object_key}")
        model_buffer.seek(0)
        model = pickle.load(model_buffer)
        print("Model successfully loaded.")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def load_metrics_from_s3(bucket_name, object_key):
    """Load metrics data from S3."""
    s3 = boto3.client('s3')
    file_buffer = BytesIO()
    try:
        s3.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=file_buffer)
        print(f"Metrics file successfully downloaded from s3://{bucket_name}/{object_key}")
        file_buffer.seek(0)
        data_str = file_buffer.getvalue().decode('utf-8')
        data = pd.read_json(StringIO(data_str), lines=True)
        print("Metrics successfully loaded into DataFrame.")
        return data
    except Exception as e:
        print(f"Error loading metrics: {str(e)}")
        raise

def preprocess_metrics(data):
    """Preprocess metrics data for forecasting."""
    try:
        data['start'] = pd.to_datetime(data['start'], errors='coerce')  # Convert 'start' column to datetime
        data['target_value'] = data['target'].apply(lambda x: x[0] if isinstance(x, list) else None)
        data = data[['start', 'target_value']].dropna()  # Drop rows with NaN target_value
        data.set_index('start', inplace=True)
        return data
    except Exception as e:
        print(f"Error during preprocessing: {str(e)}")
        raise

# Load the ARIMA model when the app starts
model = load_model_from_s3(model_bucket, model_key)

@app.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint for SageMaker."""
    return jsonify({"status": "Healthy"}), 200

@app.route('/invocations', methods=['POST'])
def predict():
    """Perform prediction using metrics data."""
    input_data = request.get_json()

    try:
        # Load and preprocess metrics data from S3
        metrics_data = load_metrics_from_s3(metrics_bucket, metrics_key)
        preprocessed_data = preprocess_metrics(metrics_data)

        # Make predictions using the ARIMA model
        forecast_steps = len(preprocessed_data)
        forecast = model.forecast(steps=forecast_steps)

        # Return predictions in the response
        return jsonify({'predictions': forecast.tolist()}), 200
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
