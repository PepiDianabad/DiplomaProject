variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "cluster_name" {
  description = "EKS Cluster Name"
  type        = string
  default     = "eks-cluster"
}

variable "cluster_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "desired_capacity" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "min_capacity" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}

variable "node_group_instance_type" {
  description = "Instance type for EKS Node Group"
  type = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "Key pair name for SSH access to worker nodes"
  type        = string
  default     = "SSH_KEY_PPETROV"
}

variable "vpc_id" {
  description = "VPC ID for the EKS Cluster"
  type        = string
  default     = "vpc-0bb7b1dd2c6f0cfff"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "Public subnets CIDR blocks"
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnets" {
  description = "Private subnets CIDR blocks"
  default     = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
}



