provider "aws" {
  region = "eu-central-1"
}

data "aws_eks_cluster" "example" {
  name = "interview-prep-eks-cluster"  # eks cluster name
}

data "aws_eks_cluster_auth" "example" {
  name = "interview-prep-eks-cluster"  # eks cluster name
}


# module "prometheus" {
#   source = "terraform-aws-modules/prometheus/aws"
#   # Add other required configurations for the Prometheus module
# }
