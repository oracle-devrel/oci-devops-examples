resource "oci_identity_policy" "devopspolicy" {
  name           = "${var.compartment_name}_devopspolicies"
  description    = "policy created for devops"
  compartment_id = var.compartment_ocid

  statements = [
    "Allow ${var.compartment_name}_devops_dg to manage all-resources in compartment id ${var.compartment_ocid}"
  ]
}