resource "aws_iam_role" "sagemaker_execution_role" {
  name = "sagemaker-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = { Service = "sagemaker.amazonaws.com" },
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "sagemaker_policy" {
  name = "sagemaker-access-policy"
  role = aws_iam_role.sagemaker_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # Access to model S3 Bucket
      {
        Effect   = "Allow",
        Action   = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::arima-model",         # S3 bucket
          "arn:aws:s3:::arima-model/*"        # Objects in the bucket
        ]
      },
      # Access to metrics S3 Bucket
      {
        Effect   = "Allow",
        Action   = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::ppetrov-prometheus-metrics-s3", # S3 bucket
          "arn:aws:s3:::ppetrov-prometheus-metrics-s3/*" # Objects in the bucket
        ]
      },
      # CloudWatch Logs permissions
      {
        Effect   = "Allow",
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      },
      # SageMaker permissions
      {
        Effect   = "Allow",
        Action   = "sagemaker:*",
        Resource = "*"
      },
      # ECR Permissions
      {
        Effect = "Allow",
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage"
        ],
        Resource = "arn:aws:ecr:eu-central-1:722377226063:repository/arima-model-repo"
      },
      {
        Effect = "Allow",
        Action = "ecr:GetAuthorizationToken",
        Resource = "*"
      },
      # SNS Publish permissions for prediction alerts
      {
        Effect   = "Allow",
        Action   = "SNS:Publish",
        Resource = "arn:aws:sns:eu-central-1:722377226063:prediction-alerts"
      }
    ]
  })
}


