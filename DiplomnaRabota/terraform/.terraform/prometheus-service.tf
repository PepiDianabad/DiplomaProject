resource "kubernetes_service" "prometheus" {
  metadata {
    name      = "prometheus-kube-prometheus-prometheus"
    namespace = "monitoring"
    labels = {
      app                         = "kube-prometheus-stack-prometheus"
      "app.kubernetes.io/instance" = "prometheus"
      "app.kubernetes.io/managed-by" = "Helm"
      "app.kubernetes.io/part-of" = "kube-prometheus-stack"
      "app.kubernetes.io/version" = "45.7.1"
      chart                       = "kube-prometheus-stack-45.7.1"
      heritage                    = "Helm"
      release                     = "prometheus"
      "self-monitor"              = "true"
    }
    annotations = {
      "kubectl.kubernetes.io/last-applied-configuration" = "{\"apiVersion\":\"v1\",\"kind\":\"Service\",\"metadata\":{\"annotations\":{\"meta.helm.sh/release-name\":\"prometheus\",\"meta.helm.sh/release-namespace\":\"monitoring\"},\"creationTimestamp\":\"2024-11-27T16:50:52Z\",\"labels\":{\"app\":\"kube-prometheus-stack-prometheus\",\"app.kubernetes.io/instance\":\"prometheus\",\"app.kubernetes.io/managed-by\":\"Helm\",\"app.kubernetes.io/part-of\":\"kube-prometheus-stack\",\"app.kubernetes.io/version\":\"45.7.1\",\"chart\":\"kube-prometheus-stack-45.7.1\",\"heritage\":\"Helm\",\"release\":\"prometheus\",\"self-monitor\":\"true\"},\"name\":\"prometheus-kube-prometheus-prometheus\",\"namespace\":\"monitoring\",\"resourceVersion\":\"1356503\",\"uid\":\"6d3ae4ba-2344-47eb-84f7-94a414b74307\"}"
    }
  }

  spec {
    ports {
      name       = "http-web"
      port       = 9090
      target_port = 9090
      protocol   = "TCP"
    }

    selector = {
      "app.kubernetes.io/name" = "prometheus"
      "app.kubernetes.io/instance" = "prometheus"  # This should match the instance name or app label
    }

    session_affinity = "None"
    type            = "LoadBalancer"
  }
}
