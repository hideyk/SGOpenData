terraform {
  required_version = ">= 1.9.5"
  required_providers {
    google = {
        version = ">= 5.42.0"
    }
  }
  backend "gcs" {
  }
}

provider "google" {
  project     = var.project_id
  region      = "ap-southeast1"
}