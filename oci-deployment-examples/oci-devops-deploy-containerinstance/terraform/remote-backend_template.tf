terraform {
  backend "s3" {
    bucket   = "${BUCKET_NAME}"
    key      = "${CONTAINERINSTANCE_DISPLAY_NAME}_terraform.tfstate"
    region   = "${REGION}"
    endpoint = "https://${NAMESPACE_NAME}.compat.objectstorage.${REGION}.oraclecloud.com"
    shared_credentials_file     = "./cred_store"
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    force_path_style            = true
  }
}