# Lambda Function Role
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Lambda Role Policies (Add S3 Write Permission)
resource "aws_iam_role_policy_attachment" "lambda_s3_write" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"  # Or a more restrictive policy with only s3:PutObject
}


# Lambda Function
resource "aws_lambda_function" "my_lambda" {
  function_name    = "my_lambda_function"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "lambda_function.lambda_handler"
  filename         = "./modules/lambda/lambda_function.zip" # Pre-zipped Python code
  source_code_hash = filebase64sha256("./modules/lambda/lambda_function.zip")
  
  # Environment Variables (optional)
  environment {
    variables = {
      BUCKET_NAME = "my-s3-bucket"
    }
  }
}

# S3 Bucket to Upload Lambda Code
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "ppetrov-lambda-function-bucket"
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_bucket.bucket
  key    = "lambda_function.zip"
  source = "./modules/lambda/lambda_function.zip" # Local file path
}

