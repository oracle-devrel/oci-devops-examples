terraform {
  required_version = ">= 1.0"
  required_providers {
    oci = {
      source  = "oracle/oci"
    }
  }
}

provider "oci" {
  auth = "ResourcePrincipal"
  region = "${var.oci_region}"
}