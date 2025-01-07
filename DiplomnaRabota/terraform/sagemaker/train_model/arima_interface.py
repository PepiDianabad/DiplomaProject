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
sns_topic_arn = "arn:aws:sns:eu-central-1:722377226063:predition-alerts"  # Replace with your SNS Topic ARN
prediction_threshold = 0.40  # Replace with your desired threshold

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
        # Assuming JSONL format (one JSON object per line)
        data = pd.read_json(StringIO(data_str), lines=True)
        print("Metrics successfully loaded into DataFrame.")

        print("First rows:")
        print(data.head())

        print("Last 3 rows of data:")
        print(data.tail(3))

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

def send_sns_notification(predictions):
    """Send an SNS notification if predictions exceed the threshold."""
    sns = boto3.client('sns')
    try:
        message = (
            f"Attention: The predicted values have exceeded the threshold ({prediction_threshold}).\n"
            f"Predictions: {predictions}"
        )
        response = sns.publish(
            TopicArn=sns_topic_arn,
            Subject="Alert: Prediction Threshold Exceeded",
            Message=message
        )
        print("SNS Notification sent successfully:", response)
    except Exception as e:
        print(f"Error sending SNS notification: {str(e)}")
        raise

@app.route('/invocations', methods=['POST'])
def predict():
    """Perform prediction using metrics data."""
    try:
        # Load and preprocess metrics data from S3
        metrics_data = load_metrics_from_s3(metrics_bucket, metrics_key)
        preprocessed_data = preprocess_metrics(metrics_data)

        # Split data into train and test sets (80-20 split)
        train_size = int(len(preprocessed_data) * 0.8)
        train_data = preprocessed_data[:train_size]
        test_data = preprocessed_data[train_size:]

        # Fit the ARIMA model on the training data
        arima_model = ARIMA(train_data['target_value'], order=(5, 1, 0)) 
        model_fit = arima_model.fit()

        # Make predictions on the test set
        forecast = model_fit.forecast(steps=len(test_data))

        # Make future predictions (next 6 scrapes - 30 mins)
        forecast_steps = 6  # Number of future steps to predict
        future_forecast = model_fit.forecast(steps=forecast_steps)

        # Check if predictions exceed the threshold
        if any(value > prediction_threshold for value in future_forecast):
            send_sns_notification(future_forecast.tolist())

        # Return predictions in the response
        return jsonify({
            'predictions': forecast.tolist(),
            'future_predictions': future_forecast.tolist(),
            'threshold': prediction_threshold
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
