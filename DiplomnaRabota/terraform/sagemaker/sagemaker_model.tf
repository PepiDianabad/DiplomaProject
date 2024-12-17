# provider "aws" {
#   region = "eu-central-1" # Replace with your AWS region
# }

# # SageMaker Model
# resource "aws_sagemaker_model" "model" {
#   name                 = "ppetrov-arima-sagemaker-model"
#   execution_role_arn   = aws_iam_role.sagemaker_execution_role.arn

#   primary_container {
#     image   = var.ecr_image_uri
#     mode    = "SingleModel"
#     model_data_url = var.s3_model_path # S3 path to the .pkl file
#   }
# }

# # Endpoint Configuration
# resource "aws_sagemaker_endpoint_configuration" "endpoint_config" {
#   name = "ppetrov-endpoint-config"

#   production_variants {
#     variant_name     = "AllTraffic"
#     model_name       = aws_sagemaker_model.model.name
#     initial_instance_count = 1
#     instance_type         = "ml.m5.large" # Choose instance type based on your workload
#   }
# }

# # SageMaker Endpoint
#  resource "aws_sagemaker_endpoint" "endpoint" {
#    name              = "ppetrov-endpoint"
#    endpoint_config_name = aws_sagemaker_endpoint_configuration.endpoint_config.name
#  }
