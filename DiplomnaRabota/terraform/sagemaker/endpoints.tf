resource "aws_sagemaker_endpoint_configuration" "deepar_endpoint_config" {
  name = "deepar-endpoint-config"

  production_variants {
    variant_name          = "AllTraffic"
    model_name            = aws_sagemaker_model.deepar_model.name
    instance_type         = "ml.m5.large"
    initial_instance_count = 1
  }
}

resource "aws_sagemaker_endpoint" "deepar_endpoint" {
  name                  = "deepar-endpoint"
  endpoint_config_name  = aws_sagemaker_endpoint_configuration.deepar_endpoint_config.name
}
