data "aws_eks_cluster" "example" {
  name = "interview-prep-eks-cluster"  # EKS cluster name
}
data "aws_eks_cluster_auth" "example" {
  name = "interview-prep-eks-cluster"  # EKS cluster name
}
# Fetch subnets dynamically based on the VPC
data "aws_subnets" "example" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
}