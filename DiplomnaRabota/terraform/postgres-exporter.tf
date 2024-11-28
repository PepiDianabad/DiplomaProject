# PostgreSQL Exporter Deployment
resource "kubernetes_deployment" "postgres_exporter" {
  metadata {
    name      = "postgres-exporter"
    namespace = kubernetes_namespace.app.metadata[0].name  # Same namespace as your app
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "postgres-exporter"
      }
    }
    template {
      metadata {
        labels = {
          app = "postgres-exporter"
        }
      }
      spec {
        container {
          name  = "postgres-exporter"
          image = "wrouesnel/postgres_exporter:latest"
          port {
            container_port = 9187  # Default port for the PostgreSQL Exporter metrics
          }
          env {
            name  = "DATA_SOURCE_NAME"
            value = "postgresql://postgres:password@postgres:5432/interview_prep_db?sslmode=disable"  # Adjust connection string as needed
          }
        }
      }
    }
  }
}

# PostgreSQL Exporter Service
resource "kubernetes_service" "postgres_exporter" {
  metadata {
    name      = "postgres-exporter"
    namespace = kubernetes_namespace.app.metadata[0].name  # Same namespace as your app
  }
  spec {
    selector = {
      app = "postgres-exporter"
    }
    port {
      port        = 9187
      target_port = 9187
    }
    type = "ClusterIP"
  }
}
