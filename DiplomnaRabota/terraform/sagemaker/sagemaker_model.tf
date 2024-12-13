resource "aws_sagemaker_model" "deepar_model" {
  name               = "deepar-model"
  execution_role_arn = aws_iam_role.sagemaker_execution_role.arn
  primary_container {
    image = "811284229333.dkr.ecr.eu-central-1.amazonaws.com/sagemaker-deepar:latest"
    model_data_url  = "s3://${aws_s3_bucket.sagemaker_data_bucket.bucket}/artifacts/output.tar.gz"
  }
}
