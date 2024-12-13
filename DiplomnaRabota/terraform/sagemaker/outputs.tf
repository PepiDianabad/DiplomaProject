output "sagemaker_model_name" {
  value = aws_sagemaker_model.deepar_model.name
}

output "sagemaker_endpoint_name" {
  value = aws_sagemaker_endpoint.deepar_endpoint.name
}

output "sagemaker_execution_role_arn" {
  value = aws_iam_role.sagemaker_execution_role.arn
}
