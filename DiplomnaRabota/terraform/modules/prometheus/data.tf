data "aws_eks_cluster" "example" {
  name = "interview-prep-eks-cluster"  # EKS cluster name
}

data "aws_eks_cluster_auth" "example" {
  name = "interview-prep-eks-cluster"  # EKS cluster name
}

data "aws_vpc" "example" {
  id = "vpc-0076a3641ca670234"
}
# Fetch subnets dynamically based on the VPC
data "aws_subnets" "example" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
}