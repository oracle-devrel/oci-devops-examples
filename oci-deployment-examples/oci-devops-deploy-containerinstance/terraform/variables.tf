variable "oci_region" {
  default = "${REGION}"
}
variable "compartment_ocid" {
  default = "${COMPARTMENT_OCID}"
}

variable "availability_domain" {
  default = "${AD}"
}

variable "graceful_shutdown_timeout_in_seconds" {
  default = 0
}

variable "instance_display_name" {
  default = "${CONTAINERINSTANCE_DISPLAY_NAME}"
}

variable "shape" {
  default = "CI.Standard.E4.Flex"
}

variable "c1_additional_capabilities" {
  default = []
}

variable "c1_arguments" {
  default = []
}

variable "c1_command" {
  default = []
}

variable "c1_display_name" {
  default = "python_fast_app"
}

variable "c1_environment_variables" {
  default = {
    "version" = "${BUILDRUN_HASH}"
    "instance_name"        = "${CONTAINERINSTANCE_DISPLAY_NAME}"

  }
}

variable "c1_iaage_url" {
  default = "${CONTAINER_REGISTRY_URL}"
}

variable "c1_image_static_tag" {
        default = "${IMAGE_STATIC_TAG}"
}

variable "c1_is_resource_principal_disabled" {
  default = false
}

variable "memory_in_gbs" {
  default = 1
}

variable "ocpus" {
  default = 1
}

variable "is_public_ip_assigned" {
  default = true
}

variable "skip_source_dest_check" {
  default = true
}

variable "subnet_id" {
  default = "${SUBNET_OCID}"
}