import pandas as pd
import pickle
from prophet import Prophet
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Step 1: Load the Trained Model from the File
with open('prophet_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Step 2: Define Test Data (10-15 lines)
data = [
    {"ds": "2024-12-14T00:36:00Z", "y": 0.03711930513968954},
    {"ds": "2024-12-14T00:39:00Z", "y": 0.037231166727584355},
    {"ds": "2024-12-14T00:42:00Z", "y": 0.03734302831547917},
    {"ds": "2024-12-14T00:45:00Z", "y": 0.037454889903373986},
    {"ds": "2024-12-14T00:48:00Z", "y": 0.0375667514912688},
    {"ds": "2024-12-14T00:51:00Z", "y": 0.03767861307916362},
    {"ds": "2024-12-14T00:54:00Z", "y": 0.037790474667058434},
    {"ds": "2024-12-14T00:57:00Z", "y": 0.03790233625495325},
    {"ds": "2024-12-14T01:00:00Z", "y": 0.038014197842848064},
    {"ds": "2024-12-14T01:03:00Z", "y": 0.03812605943074288},
    {"ds": "2024-12-14T01:06:00Z", "y": 0.0382379210186377},
    {"ds": "2024-12-14T01:09:00Z", "y": 0.03834978260653252},
    {"ds": "2024-12-14T01:12:00Z", "y": 0.03846164419442734},
    {"ds": "2024-12-14T01:15:00Z", "y": 0.03857350578232216}
]

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Step 3: Convert 'ds' column to datetime format
df['ds'] = pd.to_datetime(df['ds'])
df['ds'] = df['ds'].dt.tz_localize(None)  # Remove timezone info if present

# Step 4: Use Prophet's `make_future_dataframe` to get future predictions
future = model.make_future_dataframe(df, periods=10, freq='minute')  # Remove `include_history` as it's True by default

# Step 5: Predict using the trained model
forecast = model.predict(future)

# Step 6: Evaluate the Model's Performance
y_true = df['y']
y_pred = forecast['yhat'].values

# Calculate error metrics
mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mape = mean_absolute_percentage_error(y_true, y_pred)

# Print the error metrics
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"Mean Absolute Percentage Error (MAPE): {mape}")

# Step 7: Display Predictions in Console
print("\nPredictions vs Actual Values:")
for actual, predicted in zip(y_true, y_pred):
    print(f"Actual: {actual}, Predicted: {predicted}")
