resource "oci_identity_policy" "devopspolicy" {
  provider       = oci.home_region
  name           = "${var.compartment_name}_devopspolicies"
  description    = "policy created for devops"
  compartment_id = var.compartment_ocid

  statements = [
    "Allow group Administrators to manage devops-family in compartment id ${var.compartment_ocid}",
    "Allow group Administrators to manage all-artifacts in compartment id ${var.compartment_ocid}",
    "Allow  dynamic-group devops_dg_${var.compartment_name} to manage all-resources in compartment id ${var.compartment_ocid}",
  ]
}