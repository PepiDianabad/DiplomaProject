provider "aws" {
  region = "eu-central-1" # Replace with your AWS region
}

# SageMaker Model
resource "aws_sagemaker_model" "model" {
  name               = "ppetrov-arima-sagemaker-model"
  execution_role_arn = aws_iam_role.sagemaker_execution_role.arn

  primary_container {
    image        = var.ecr_image_uri
    mode         = "SingleModel"
    model_data_url = var.s3_model_path # S3 path to the .pkl file
  }
}

resource "aws_sagemaker_endpoint_configuration" "endpoint_config" {
  name = "ppetrov-endpoint-config"

  production_variants {
    variant_name          = "AllTraffic"
    model_name            = aws_sagemaker_model.model.name
    initial_instance_count = 1
    instance_type         = "ml.m5.large"
  }

  data_capture_config {
    enable_capture             = true
    initial_sampling_percentage = 100
    destination_s3_uri         = "s3://arima-model/logs/"
    capture_options {
      capture_mode = "Input"
    }
    capture_options {
      capture_mode = "Output"
    }
  }
}

# SageMaker Endpoint
resource "aws_sagemaker_endpoint" "endpoint" {
  name                  = "ppetrov-endpoint"
  endpoint_config_name   = aws_sagemaker_endpoint_configuration.endpoint_config.name
}

# IAM Policy for CloudWatch Logs Permissions
resource "aws_iam_policy" "sagemaker_cloudwatch_policy" {
  name        = "sagemaker-cloudwatch-logs-policy"
  description = "Policy to allow SageMaker to write to CloudWatch logs"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_policy_attachment" {
  policy_arn = aws_iam_policy.sagemaker_cloudwatch_policy.arn
  role       = aws_iam_role.sagemaker_execution_role.name
}
