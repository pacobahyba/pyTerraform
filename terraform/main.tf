provider "google" {
  project = var.project_id
  region  = "us-central1"
}

# 1. Artifact Registry para a imagem Docker do Backend
resource "google_artifact_registry_repository" "repo" {
  location      = "us-central1"
  repository_id = "reflex-repo"
  format        = "DOCKER"
}

# 2. Serviço Cloud Run para o Backend (API)
resource "google_cloud_run_service" "app" {
  name     = "py-terraform-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/${var.project_id}/reflex-repo/py-terraform:latest"
        ports {
          container_port = 8000
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# 3. Permissão de acesso público para o Cloud Run
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.app.name
  location = google_cloud_run_service.app.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# 4. Bucket para o Frontend Estático
resource "google_storage_bucket" "frontend_static" {
  name                        = "frontend-pyterraform-${var.project_id}"
  location                    = "us-central1"
  force_destroy               = true
  uniform_bucket_level_access = true

  # CONFIGURAÇÃO CRÍTICA PARA SPA (Single Page Application)
  website {
    main_page_suffix = "index.html"
    # Redireciona erros de rota para o index.html para o React assumir o controlo
    not_found_page   = "index.html" 
  }

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "OPTIONS"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# 5. Permissão de leitura pública para o Bucket
resource "google_storage_bucket_iam_member" "public_bucket_access" {
  bucket = google_storage_bucket.frontend_static.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# Outputs
output "backend_url" {
  value = google_cloud_run_service.app.status[0].url
}

output "frontend_url" {
  value = "https://storage.googleapis.com/${google_storage_bucket.frontend_static.name}/index.html"
}