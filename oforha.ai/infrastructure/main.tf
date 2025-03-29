terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "oforha-ai"
  region  = "us-central1"
}

# Cloud Run service for API
resource "google_cloud_run_service" "api" {
  name     = "oforha-api"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/oforha-ai/api:latest"
        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
        env {
          name  = "NODE_ENV"
          value = "production"
        }
      }
    }
  }
}

# Cloud SQL instance
resource "google_sql_database_instance" "main" {
  name             = "oforha-db"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      authorized_networks {
        name  = "all"
        value = "0.0.0.0/0"
      }
    }
  }
}

# Storage bucket for static assets
resource "google_storage_bucket" "static" {
  name     = "oforha-static"
  location = "US"

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  cors {
    origin          = ["https://oforha.com"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# Vertex AI workspace
resource "google_vertex_ai_dataset" "training" {
  display_name = "oforha-training-data"
  metadata_schema_uri = "gs://google-cloud-aiplatform/schema/dataset/metadata/text_1.0.0.yaml"
  region = "us-central1"
} 