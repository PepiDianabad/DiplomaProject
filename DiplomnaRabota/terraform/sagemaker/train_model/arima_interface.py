import pickle
import boto3
import pandas as pd
from flask import Flask, request, jsonify
from statsmodels.tsa.arima.model import ARIMA
from io import BytesIO

app = Flask(__name__)

def model_fn(model_dir):
    """Load the trained model from S3"""
    s3 = boto3.client('s3')
    bucket_name = model_dir.split('/')[0]
    object_key = '/'.join(model_dir.split('/')[1:]) + 'arima_model.pkl'

    model_buffer = BytesIO()
    s3.download_fileobj(Bucket=bucket_name, Key=object_key, Fileobj=model_buffer)

    model_buffer.seek(0)
    model = pickle.load(model_buffer)
    return model

model = model_fn('arima-model')

@app.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint"""
    return jsonify({"status": "Healthy"}), 200

@app.route('/invocations', methods=['POST'])
def predict():
    """Perform prediction using the loaded ARIMA model"""
    input_data = request.get_json()
    timestamp = input_data.get("timestamp")
    value = input_data.get("value")
    
    if not timestamp or not value:
        return jsonify({"error": "Invalid input data"}), 400

    input_df = pd.DataFrame({'timestamp': timestamp, 'value': value})
    input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])
    input_df.set_index('timestamp', inplace=True)

    forecast = model.forecast(steps=len(input_df))
    return jsonify({'predictions': forecast.tolist()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
