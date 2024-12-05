resource "aws_sagemaker_model" "my_model" {
  name               = "failure-prediction-model"
  execution_role_arn = aws_iam_role.sagemaker_execution.arn

  primary_container {
    image           = "763104351884.dkr.ecr.us-east-1.amazonaws.com/xgboost:1.5-1"
    model_data_url  = "s3://${aws_s3_bucket.sagemaker_bucket.bucket}/models/my_model.tar.gz"
  }

  tags = {
    Environment = "Production"
  }
}
