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

resource "aws_iam_role_policy_attachment" "sagemaker_policy_attachment" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = aws_iam_policy.sagemaker_policy.arn
}
