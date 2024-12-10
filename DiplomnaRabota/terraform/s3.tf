resource "aws_s3_bucket" "prometheus_metrics" {
  bucket = "ppetrov-prometheus-metrics-s3"
  acl    = "private"

  tags = {
    Environment = var.environment
  }
}

output "s3_bucket_name" {
  value = aws_s3_bucket.prometheus_metrics.bucket
}
