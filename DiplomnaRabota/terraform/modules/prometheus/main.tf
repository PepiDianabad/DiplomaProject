provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.example.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.example.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.example.token
  }
}

# Create a Helm release for Prometheus
resource "helm_release" "prometheus" {
  name       = "prometheus"
  namespace  = "monitoring"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  version    = "45.7.1"  # Replace with a valid version you found

  values = [
    <<EOF
    prometheus:
      prometheusSpec:
        serviceMonitorSelectorNilUsesHelmValues: false
    EOF
  ]

depends_on = [
  data.aws_eks_cluster.example  # Use data source instead of resource
]
}

# You can add more resources like ServiceAccounts, ConfigMaps if needed for the Prometheus setup
