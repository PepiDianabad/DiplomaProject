resource "aws_sagemaker_training_job" "deepar_training" {
  name              = "deepar-training-job"
  role_arn          = aws_iam_role.sagemaker_execution_role.arn
  algorithm_specification {
    training_image       = "382416733822.dkr.ecr.eu-central-1.amazonaws.com/deepar:latest"
    training_input_mode  = "File"
  }

  input_data_config {
    channel_name = "train"
    data_source {
      s3_data_source {
        s3_data_type   = "S3Prefix"
        s3_uri         = "s3://ppetrov-prometheus-metrics-s3/metrics/"
        s3_data_distribution_type = "FullyReplicated"
      }
    }
    content_type = "application/jsonlines"
  }

  output_data_config {
    s3_output_path = "s3://${aws_s3_bucket.sagemaker_model_bucket.bucket}/artifacts/"
  }

  resource_config {
    instance_type  = "ml.m5.large"
    instance_count = 1
    volume_size    = 10
  }

  stopping_condition {
    max_runtime_in_seconds = 3600
  }

  hyperparameters = {
    "time_freq"         = "5min"
    "context_length"    = "12"
    "prediction_length" = "12"
    "epochs"            = "50"
    "mini_batch_size"   = "64"
    "learning_rate"     = "0.001"
  }
}
