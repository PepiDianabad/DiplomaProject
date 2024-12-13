output "sagemaker_model_name" {
  value = aws_sagemaker_model.depar_model.name
}

output "sagemaker_endpoint_name" {
  value = aws_sagemaker_endpoint.depar_endpoint.name
}

output "sagemaker_execution_role_arn" {
  value = aws_iam_role.sagemaker_execution_role.arn
}
