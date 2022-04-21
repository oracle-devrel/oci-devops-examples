terraform {
  backend "s3" {
    bucket   = "mr-prod-objectstore-for-terraform"
    key      = "${compartment_name}/terraform.tfstate"
    region   = "us-ashburn-1"
    endpoint = "https://fahdabidiroottenancy.compat.objectstorage.us-ashburn-1.oraclecloud.com"
    shared_credentials_file     = "./cred_store"
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    force_path_style            = true
  }
}