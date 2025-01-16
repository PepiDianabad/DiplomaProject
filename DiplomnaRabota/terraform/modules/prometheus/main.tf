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
  version    = "66.3.0"  

  values = [
    <<EOF
    prometheus:
      prometheusSpec:
        serviceMonitorSelectorNilUsesHelmValues: false
        additionalScrapeConfigs:
          - job_name: 'postgres'
            static_configs:
              - targets: ['postgres-exporter.application:9187']
          - job_name: 'node-exporter'
            static_configs:
              - targets: ['node-exporter.monitoring.svc.cluster.local:9100']
    prometheusService:
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp
        service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
    EOF
  ]

  timeout = 300  # timeout in seconds (5 minutes = 300 seconds)

  depends_on = [
    data.aws_eks_cluster.example  # data source instead of resource
  ]
}