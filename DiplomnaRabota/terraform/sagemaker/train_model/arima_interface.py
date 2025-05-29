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
sns_topic_arn = "arn:aws:sns:eu-central-1:722377226063:prediction-alerts"  # Replace with your SNS Topic ARN
node_thresholds = {
    1: 0.05,  # Threshold for Node 1
    2: 0.04,  # Threshold for Node 2
    3: 0.42   # Threshold for Node 3
}

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
        data['start'] = pd.to_datetime(data['start'], errors='coerce')  
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

def send_sns_notification(node_exceedances):
    """Send an SNS notification if predictions for any node exceed their thresholds."""
    sns = boto3.client('sns')
    try:
        message = "Attention: Prediction thresholds exceeded for the following nodes:\n"
        for node, predictions in node_exceedances.items():
            message += f"Node {node}: {predictions}\n"
        
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
        metrics_data = load_metrics_from_s3(metrics_bucket, metrics_key)
        preprocessed_data = preprocess_metrics(metrics_data)

        # Split data into train and test sets (80-20 split)
        train_size = int(len(preprocessed_data) * 0.8)
        train_data = preprocessed_data[:train_size]
        test_data = preprocessed_data[train_size:]

        print(train_data)

        # Fit the ARIMA model on the training data
        arima_model = ARIMA(train_data['target_value'], order=(5, 1, 0)) 
        model_fit = arima_model.fit()

        # Make predictions on the test set
        forecast = model_fit.forecast(steps=len(test_data))

        # Make future predictions (next 6 scrapes - 30 mins)
        forecast_steps = 6  # Number of future steps to predict
        future_forecast = model_fit.forecast(steps=forecast_steps)

        # Group predictions by nodes (e.g., 1st, 2nd, 3rd values correspond to Node 1, Node 2, Node 3)
        node_predictions = {node: [] for node in node_thresholds.keys()}
        for i, prediction in enumerate(future_forecast):
            node_id = (i % len(node_thresholds)) + 1  # Map prediction index to node ID (1, 2, 3)
            node_predictions[node_id].append(prediction)

        # Check if predictions exceed the thresholds for each node
        node_exceedances = {}
        for node, predictions in node_predictions.items():
            exceedances = [value for value in predictions if value > node_thresholds[node]]
            if exceedances:
                node_exceedances[node] = exceedances

        # Send notification if any node exceeds its threshold
        if node_exceedances:
            send_sns_notification(node_exceedances)

        # Return predictions in the response
        return jsonify({
            'predictions': forecast.tolist(),
            'future_predictions': future_forecast.tolist(),
            'node_predictions': node_predictions
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
