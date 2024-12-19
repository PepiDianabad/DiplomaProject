import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from pmdarima import auto_arima
import boto3
import joblib
from io import BytesIO

# Hardcoded dataset (example data)
def create_hardcoded_data():
    data = [
        {'start': '2024-01-01 00:00:00', 'target_value': 100},
        {'start': '2024-01-01 01:00:00', 'target_value': 110},
        {'start': '2024-01-01 02:00:00', 'target_value': 120},
        {'start': '2024-01-01 03:00:00', 'target_value': 130},
        {'start': '2024-01-01 04:00:00', 'target_value': 140},
        {'start': '2024-01-01 05:00:00', 'target_value': 150},
        {'start': '2024-01-01 06:00:00', 'target_value': 160},
        {'start': '2024-01-01 07:00:00', 'target_value': 170},
        {'start': '2024-01-01 08:00:00', 'target_value': 180},
        {'start': '2024-01-01 09:00:00', 'target_value': 190},
        {'start': '2024-01-01 10:00:00', 'target_value': 200},
        {'start': '2024-01-01 11:00:00', 'target_value': 210},
    ]
    df = pd.DataFrame(data)
    df['start'] = pd.to_datetime(df['start'])
    df = df.set_index('start')
    return df

# Fit ARIMA model using auto_arima
def fit_arima(data):
    model = auto_arima(data['target_value'], seasonal=False, stepwise=True, trace=True)
    model_fit = model.fit(data['target_value'])
    return model_fit

# Test the model's performance
def test_model(model_fit, train_data, test_data):
    forecast = model_fit.predict(n_periods=len(test_data))
    y_true = test_data['target_value']
    y_pred = forecast
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    
    print(f"Test results for ARIMA model:")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape}%")

def save_model_to_s3(model, bucket_name, model_filename):
    # Save the ARIMA model using joblib
    with BytesIO() as model_buffer:
        joblib.dump(model, model_buffer)
        model_buffer.seek(0)
        
        # Upload the model to S3
        s3 = boto3.client('s3')
        s3.upload_fileobj(model_buffer, bucket_name, model_filename)
        print(f"Model saved to S3 as {model_filename}")

def main():
    # Create hardcoded data
    data = create_hardcoded_data()

    # Split data into train and test sets (e.g., 80% train, 20% test)
    train_size = int(len(data) * 0.8)
    train_data = data.iloc[:train_size]
    test_data = data.iloc[train_size:]

    # Train the ARIMA model
    model_fit = fit_arima(train_data)
    
    # Test the model
    test_model(model_fit, train_data, test_data)

    # Save the trained model to S3
    bucket_name = 'arima-model'  # Replace with your actual S3 bucket name
    model_filename = 'arima_model.joblib'  # Desired filename in S3
    save_model_to_s3(model_fit, bucket_name, model_filename)

if __name__ == "__main__":
    main()
