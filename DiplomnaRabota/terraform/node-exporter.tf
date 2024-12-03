resource "kubernetes_daemon_set_v1" "node_exporter" {
  metadata {
    name      = "node-exporter"
    namespace = "monitoring"
    labels = {
      app = "node-exporter"
    }
  }

  spec {
    selector {
      match_labels = {
        app = "node-exporter"
      }
    }

    template {
      metadata {
        labels = {
          app = "node-exporter"
        }
      }

      spec {
        container {
          name  = "node-exporter"
          image = "prom/node-exporter"

          port {
            container_port = 9100
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "node_exporter" {
  metadata {
    name      = "node-exporter"
    namespace = "monitoring"
  }

  spec {
    selector = {
      app = "node-exporter"
    }

    port {
      protocol = "TCP"
      port     = 9100
      target_port = 9100
    }
  }
}
