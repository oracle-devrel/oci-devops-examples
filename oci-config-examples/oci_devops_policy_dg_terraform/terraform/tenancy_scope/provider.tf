provider "oci" {
   auth = "ResourcePrincipal"
   alias  = "home_region"
   region = "${var.region}"
}