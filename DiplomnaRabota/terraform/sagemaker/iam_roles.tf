# ECR Repository
resource "aws_ecr_repository" "deepar" {
  name = "sagemaker-deepar"
}

# SageMaker Execution Role
resource "aws_iam_role" "sagemaker_execution_role" {
  name = "SageMakerExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = { Service = "sagemaker.amazonaws.com" }
      }
    ]
  })
}

# SageMaker Access to S3 Bucket
resource "aws_iam_policy" "sagemaker_policy" {
  name        = "SageMakerPolicy"
  description = "Policy for SageMaker to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = ["s3:GetObject", "s3:PutObject"],
        Effect   = "Allow",
        Resource = [
          "${aws_s3_bucket.sagemaker_data_bucket.arn}/*",
          "arn:aws:s3:::ppetrov-prometheus-metrics-s3/*"
        ]
      }
    ]
  })
}

# Attach the policy to the SageMaker role
resource "aws_iam_role_policy_attachment" "sagemaker_policy_attachment" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = aws_iam_policy.sagemaker_policy.arn
}

# ECR Repository Policy
resource "aws_ecr_repository_policy" "deepar_repository_policy" {
  repository = aws_ecr_repository.deepar.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "AllowSageMakerAccess"
        Effect    = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
        Action   = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
        Resource = "arn:aws:ecr:eu-central-1:811284229333:repository/sagemaker-deepar"
      }
    ]
  })
}

# IAM Policy for SageMaker to pull from ECR
resource "aws_iam_policy" "sagemaker_ecr_pull_policy" {
  name        = "SageMakerECRPullPolicy"
  description = "Policy to allow SageMaker to pull images from ECR"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
        Effect    = "Allow"
        Resource  = "arn:aws:ecr:eu-central-1:811284229333:repository/sagemaker-deepar"
      }
    ]
  })
}

# Attach the pull policy to the SageMaker role
resource "aws_iam_role_policy_attachment" "sagemaker_ecr_pull_policy_attachment" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = aws_iam_policy.sagemaker_ecr_pull_policy.arn
}
