
resource "oci_container_instances_container_instance" "test_container_instance" {
  availability_domain                  = var.availability_domain
  compartment_id                       = var.compartment_ocid
  container_restart_policy             = "ALWAYS"
  defined_tags                         = {}
  display_name                         = var.instance_display_name
  freeform_tags                        = {}
  graceful_shutdown_timeout_in_seconds = var.graceful_shutdown_timeout_in_seconds
  shape                                = var.shape
  containers {
    additional_capabilities        = var.c1_additional_capabilities
    arguments                      = var.c1_arguments
    command                        = var.c1_command
    defined_tags                   = {}
    display_name                   = var.c1_display_name
    environment_variables          = var.c1_environment_variables
    freeform_tags                  = {}
    image_url                      = "${var.c1_iaage_url}:${var.c1_image_static_tag}"
    is_resource_principal_disabled = var.c1_is_resource_principal_disabled
    }
  shape_config {
    memory_in_gbs                = var.memory_in_gbs
    ocpus                        = var.ocpus
     }
  timeouts {}
  vnics {
    defined_tags           = {}
    is_public_ip_assigned  = var.is_public_ip_assigned
    skip_source_dest_check = var.skip_source_dest_check
    subnet_id              = var.subnet_id
  }
}

data  "oci_core_vnic" "vnic_0_info" {
  #Required
  vnic_id = oci_container_instances_container_instance.test_container_instance.vnics[0].vnic_id
}

output "Dev" {
  value = "Made with \u2764 by Oracle Developers"
}

output "access_ip" {
  value = "Access python application via http://${data.oci_core_vnic.vnic_0_info.public_ip_address}"
}

output "container_instance_id" {
  value = oci_container_instances_container_instance.test_container_instance.id
}



