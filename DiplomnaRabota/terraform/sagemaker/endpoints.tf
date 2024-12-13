resource "aws_sagemaker_model" "deepar_model" {
  name         = "deepar-model"
  execution_role_arn = aws_iam_role.sagemaker_execution_role.arn

  primary_container {
    image        = "382416733822.dkr.ecr.eu-central-1.amazonaws.com/deepar:latest"
    model_data_url = "s3://${aws_s3_bucket.sagemaker_model_bucket.bucket}/artifacts/output.tar.gz"
  }
}

resource "aws_sagemaker_endpoint_configuration" "deepar_endpoint_config" {
  name = "deepar-endpoint-config"

  production_variants {
    variant_name = "AllTraffic"
    model_name   = aws_sagemaker_model.deepar_model.name
    instance_type = "ml.m5.large"
    initial_instance_count = 1
  }
}

resource "aws_sagemaker_endpoint" "deepar_endpoint" {
  name              = "deepar-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.deepar_endpoint_config.name
}
