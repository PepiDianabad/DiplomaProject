import boto3
s3 = boto3.client('s3')
bucket_name = "ppetrov-prometheus-metrics-s3"
file_path = 'model_data.jsonl'
s3.upload_file(file_path, bucket_name, 'metrics/arima_data.jsonl')
