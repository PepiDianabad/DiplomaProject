import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import json
import pickle
import boto3
from io import BytesIO

# Initialize the S3 client
s3 = boto3.client('s3', region_name='eu-central-1')  

# Load the dataset from local file
def load_data(data_path):
    data = []
    with open(data_path, 'r') as file:
        for line in file:
            # Parse each line as JSON
            json_data = json.loads(line.strip())
            # Extract relevant fields
            start = json_data.get('start')
            target = json_data.get('target')[0] if json_data.get('target') else None  # Extract the first value in 'target' list
            instance = json_data.get('instance')
            # Append to data list
            data.append({'start': start, 'target_value': target, 'instance': instance})

    # Create DataFrame from the parsed data
    df = pd.DataFrame(data)
    return df

# Fit ARIMA model
def fit_arima(data):
    model = ARIMA(data['target_value'], order=(3, 1, 0))  # Adjust ARIMA order if needed
    model_fit = model.fit()
    return model_fit

# Save the model and upload it to S3
def save_model_to_s3(model_fit, bucket_name, s3_model_path):
    # Create a BytesIO buffer to hold the model
    model_buffer = BytesIO()
    
    # Save the model to the buffer using pickle
    pickle.dump(model_fit, model_buffer)
    
    # Make sure the buffer's position is at the beginning
    model_buffer.seek(0)
    
    # Upload the model to S3
    s3.upload_fileobj(model_buffer, bucket_name, s3_model_path)

def main():
    data_path = 'model_data.jsonl'  
    bucket_name = 'arima-model'  
    s3_model_path = 'arima_model.pkl'  

    # Load data from local file
    data = load_data(data_path)
    
    # Train ARIMA model
    model_fit = fit_arima(data)
    
    # Save the trained model to S3
    save_model_to_s3(model_fit, bucket_name, s3_model_path)

    print(f"Model successfully uploaded to S3 at {s3_model_path}")

if __name__ == "__main__":
    main()
