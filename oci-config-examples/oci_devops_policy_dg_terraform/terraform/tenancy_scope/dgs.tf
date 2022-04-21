resource "oci_identity_dynamic_group" "devopsgroup1" {
  provider       = oci.home_region
  name           = "${var.compartment_name}_devops_dg"
  description    = "DevOps deploy pipeline dynamic group"
  compartment_id = var.tenancy_ocid
  matching_rule  = "ALL {resource.type = 'devopsdeploypipeline', resource.compartment.id = '${var.compartment_ocid}'}"
}
