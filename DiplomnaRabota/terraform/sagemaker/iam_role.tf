# resource "aws_iam_role" "sagemaker_execution_role" {
#   name = "sagemaker-execution-role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect    = "Allow",
#         Principal = { Service = "sagemaker.amazonaws.com" },
#         Action    = "sts:AssumeRole"
#       }
#     ]
#   })
# }

# resource "aws_iam_role_policy" "sagemaker_policy" {
#   name = "sagemaker-access-policy"
#   role = aws_iam_role.sagemaker_execution_role.id

#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect   = "Allow",
#         Action   = [
#           "s3:GetObject",
#           "s3:PutObject",
#           "s3:ListBucket"
#         ],
#         Resource = [
#           "arn:aws:s3:::arima-model",             # S3 bucket
#           "arn:aws:s3:::arima-model/*"           # Objects in the bucket
#         ]
#       },
#       {
#         Effect   = "Allow",
#         Action   = [
#           "logs:CreateLogGroup",
#           "logs:CreateLogStream",
#           "logs:PutLogEvents"
#         ],
#         Resource = "arn:aws:logs:*:*:*"           # CloudWatch logs
#       },
#       {
#         Effect   = "Allow",
#         Action   = "sagemaker:*",                 # Allow all SageMaker actions
#         Resource = "*"
#       },
#       {
#         Effect   = "Allow",
#         Action   = [
#           "ecr:BatchCheckLayerAvailability",
#           "ecr:BatchGetImage",
#           "ecr:GetDownloadUrlForLayer"
#         ],
#         Resource = [
#           "arn:aws:ecr:eu-central-1:722377226063:repository/arima-model-repo",
#           "arn:aws:ecr:eu-central-1:722377226063:repository/arima-model-repo/*"
#           #"722377226063.dkr.ecr.eu-central-1.amazonaws.com/arima-model-repo@sha256:5f820537bb1e72c99ab0560993c6337b4a09529c5c22048eaf132460ce45ea41"
#         ]
#       }
#     ]
#   })
# }

# output "sagemaker_role_arn" {
#   value = aws_iam_role.sagemaker_execution_role.arn
# }
