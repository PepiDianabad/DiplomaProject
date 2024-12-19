variable "ecr_image_uri" {
  description = "URI of the ECR Image"
  type        = string
  default     = "722377226063.dkr.ecr.eu-central-1.amazonaws.com/arima-model-repo:latest"
}

variable "s3_model_path" {
  description = "S3 path to the .pkl file"
  type        = string
  default     = "s3://arima-model/model.tar.gz"  # Updated to reflect the new tar.gz file
}

