output "eks_cluster_endpoint" {
  description = "EKS Cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_name" {
  description = "EKS Cluster name"
  value       = module.eks.cluster_name
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "cluster_endpoint" {
  value = data.aws_eks_cluster.example.endpoint  
}

output "cluster_ca_certificate" {
  value = data.aws_eks_cluster.example.certificate_authority[0].data  
}

output "kubeconfig_token" {
  value = data.aws_eks_cluster_auth.example.token  
  sensitive = true
}

#sage maker outputs



