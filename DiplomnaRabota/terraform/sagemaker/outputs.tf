# In outputs.tf within the sagemaker module
output "sagemaker_bucket_name" {
  value = aws_s3_bucket.sagemaker_bucket.bucket
}

output "sagemaker_endpoint_name" {
  value = aws_sagemaker_endpoint.endpoint.name
}

output "sagemaker_model_arn" {
  value = aws_sagemaker_model.my_model.arn
}
