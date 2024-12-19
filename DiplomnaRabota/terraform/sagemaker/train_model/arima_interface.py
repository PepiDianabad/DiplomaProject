import pickle
import boto3
import pandas as pd
from flask import Flask, request, jsonify
from statsmodels.tsa.arima.model import ARIMA
from io import BytesIO, StringIO

app = Flask(__name__)

def model_fn(model_dir):
    """Load the trained ARIMA model from S3"""
    s3 = boto3.client('s3')
    
    # Extract the bucket name and model file path from model_dir
    bucket_name = model_dir.split('/')[0]
    object_key = '/'.join(model_dir.split('/')[1:]) + '/arima_model.pkl'  # Ensure path format is correct

    # Download the model from S3 into a buffer
    model_buffer = BytesIO()
    s3.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=model_buffer)

    # Load the model from the buffer using pickle
    model_buffer.seek(0)
    model = pickle.load(model_buffer)
    return model

def load_data_from_s3(s3_path):
    """Load model data from S3"""
    s3 = boto3.client('s3')
    bucket_name = s3_path.split('/')[0]
    object_key = '/'.join(s3_path.split('/')[1:])

    # Download the file into memory
    file_buffer = BytesIO()
    s3.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=file_buffer)

    # Read it into a pandas DataFrame
    file_buffer.seek(0)
    data_str = file_buffer.getvalue().decode('utf-8')
    data = pd.read_json(StringIO(data_str), lines=True)

    # Preprocess the data (similar to your local code)
    data['start'] = pd.to_datetime(data['start'], errors='coerce')  # Convert 'start' column to datetime
    data['target_value'] = data['target'].apply(lambda x: x[0] if isinstance(x, list) else None)
    data = data[['start', 'target_value']].dropna()  # Drop rows with NaN target_value
    data.set_index('start', inplace=True)
    return data

# Load the ARIMA model from S3 when the app starts
model = model_fn('arima-model')

@app.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint for SageMaker"""
    return jsonify({"status": "Healthy"}), 200

@app.route('/invocations', methods=['POST'])
def predict():
    """Perform prediction using the loaded ARIMA model"""
    input_data = request.get_json()

    # Load the data from S3 (or the request if needed)
    s3_path = input_data.get("s3_path")
    if not s3_path:
        return jsonify({"error": "Invalid input, missing 's3_path'"}), 400

    try:
        # Load the data from the specified S3 path
        data = load_data_from_s3(s3_path)
    except Exception as e:
        return jsonify({"error": f"Error loading data from S3: {str(e)}"}), 400

    # Make predictions using the ARIMA model
    forecast_steps = len(data)
    forecast = model.forecast(steps=forecast_steps)

    # Return the forecasted values in the response
    return jsonify({'predictions': forecast.tolist()}), 200

if __name__ == '__main__':
    # Run the Flask app with host set to '0.0.0.0' for SageMaker compatibility
    app.run(host='0.0.0.0', port=8081)
