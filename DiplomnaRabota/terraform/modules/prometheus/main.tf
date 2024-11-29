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
  version    = "66.3.0"  # Replace with a valid version you found

  values = [
    <<EOF
    prometheus:
      prometheusSpec:
        serviceMonitorSelectorNilUsesHelmValues: false
        additionalScrapeConfigs:
          - job_name: 'postgres'
            static_configs:
              - targets: ['postgres-exporter.application:9187']
    EOF
  ]

  timeout = 600  # Set timeout in seconds (10 minutes = 600 seconds)

  depends_on = [
    data.aws_eks_cluster.example  # Use data source instead of resource
  ]
}
