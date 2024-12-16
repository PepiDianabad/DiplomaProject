FROM python:3.9-slim

# Install Python dependencies
RUN pip install pandas statsmodels flask boto3

# Copy your model and script into the container
COPY models/arima_model.pkl /opt/ml/model/
COPY arima_interface.py /app/arima_interface.py

# Set the working directory
WORKDIR /app

# Expose the Flask app's port
EXPOSE 8080

# Run the Flask app
CMD ["python", "arima_interface.py"]
