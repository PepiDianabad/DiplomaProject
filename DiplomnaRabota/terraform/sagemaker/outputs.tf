output "sagemaker_endpoint" {
  value = aws_sagemaker_endpoint.endpoint.name
}

output "sagemaker_role_arn" {
  value = aws_iam_role.sagemaker_execution_role.arn
}
