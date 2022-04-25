resource "oci_identity_dynamic_group" "devopsgroup1" {
  provider       = oci.home_region
  name           = "devops_dg_${var.compartment_name}"
  description    = "DevOps deploy pipeline dynamic group"
  compartment_id = var.tenancy_ocid
  matching_rule  = "ALL {resource.type = 'devopsdeploypipeline', resource.compartment.id = '${var.compartment_ocid}'}"
}
