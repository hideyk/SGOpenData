module "gcs_buckets" {
  source  = "terraform-google-modules/cloud-storage/google"
  version = "~> 6.0"
  project_id  = var.project_id
  names = ["extract-artifacts"]
  location = var.location
  prefix = "sg-open-data"
  set_admin_roles = false
  public_access_prevention = "enforced"
  randomize_suffix = true
}