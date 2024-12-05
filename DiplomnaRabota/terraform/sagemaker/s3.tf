resource "aws_s3_bucket" "sagemaker_bucket" {
  bucket = "ppetrov-sagemaker-bucket"
  #acl    = "private"
}

resource "aws_s3_bucket_acl" "sagemaker_bucket_acl" {
  bucket = aws_s3_bucket.sagemaker_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.sagemaker_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

