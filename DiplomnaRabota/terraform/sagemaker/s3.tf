resource "aws_s3_bucket" "sagemaker_data_bucket" {
  bucket = "ppetrov-sagemaker-data"
  acl    = "private"

  tags = {
    Name        = "SageMaker Data Bucket"
    Environment = "Diploma"
  }
}

resource "aws_s3_bucket_policy" "sagemaker_data_bucket_policy" {
  bucket = aws_s3_bucket.sagemaker_data_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = ["s3:GetObject", "s3:PutObject"],
        Effect    = "Allow",
        Principal = { Service = "sagemaker.amazonaws.com" },
        Resource  = "${aws_s3_bucket.sagemaker_data_bucket.arn}/*"
      }
    ]
  })
}
