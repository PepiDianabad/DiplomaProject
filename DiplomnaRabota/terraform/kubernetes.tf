data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
}


provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
}

 # Namespace
 resource "kubernetes_namespace" "app" {
   metadata {
     name = "application"
   }
 }

# Backend Deployment
resource "kubernetes_deployment" "backend" {
  metadata {
    name      = "backend"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "backend"
      }
    }
    template {
      metadata {
        labels = {
          app = "backend"
        }
      }
      spec {
        container {
          image = "ppetrov06/interview_preparation_app:backend10"
          name  = "backend"
          port {
            container_port = 5000
          }
          env {
            name  = "DB_HOST"
            value = "postgres"  # This should match the PostgreSQL service name
          }
          env {
            name  = "DB_PORT"
            value = "5432"
          }
          env {
            name  = "DB_NAME"
            value = "postgres"
          }
          env {
            name  = "DB_USER"
            value = "postgres"
          }
          env {
            name  = "DB_PASSWORD"
            value = "password"
          }
        }
      }
    }
  }
}


# Backend Service
resource "kubernetes_service" "backend" {
  metadata {
    name      = "backend-service"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
  spec {
    selector = {
      app = "backend"
    }
    port {
      port        = 5000
      target_port = 5000
    }
    type = "LoadBalancer"
  }
}

# Frontend Deployment
resource "kubernetes_deployment" "frontend" {
  metadata {
    name      = "frontend"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "frontend"
      }
    }
    template {
      metadata {
        labels = {
          app = "frontend"
        }
      }
      spec {
        container {
          image = "ppetrov06/interview_preparation_app:frontend199"
          name  = "frontend"
          port {
            container_port = 3001
          }
          env {
            name  = "HOST"
            value = "0.0.0.0"  # Add this line to listen on all interfaces
          }
        }
      }
    }
  }
}

# Frontend Service
resource "kubernetes_service" "frontend" {
  metadata {
    name      = "frontend-service"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
  spec {
    selector = {
      app = "frontend"
    }
    port {
      port        = 3001
      target_port = 3000
    }
    type = "LoadBalancer"
  }
}

# PostgreSQL Deployment
resource "kubernetes_deployment" "database" {
  metadata {
    name      = "postgres"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "postgres"
      }
    }
    template {
      metadata {
        labels = {
          app = "postgres"
        }
      }
      spec {
        container {
          image = "postgres:latest"
          name  = "postgres"
          port {
            container_port = 5432
          }
          env {
            name  = "POSTGRES_USER"
            value = "postgres"
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = "password"
          }
          env {
            name  = "POSTGRES_DB"
            value = "interview_prep_db"  # Set the desired database name here
          }
        }
      }
    }
  }
}

# PostgreSQL Service
resource "kubernetes_service" "postgres" {
  metadata {
    name      = "postgres"
    namespace = kubernetes_namespace.app.metadata[0].name
  }
  spec {
    selector = {
      app = "postgres"
    }
    port {
      port        = 5432
      target_port = 5432
    }
    type = "ClusterIP"
  }
}

