variable "eks_role_arn" {
  description = "The EKS cluster role ARN"
  type        = string
}

variable "subnet_ids" {
  description = "The subnet IDs for the EKS cluster"
  type        = list(string)
}

variable "vpc_id" {
  description = "The VPC ID where the EKS cluster is located"
  type        = string
}
