variable oci_dg_name {
  type        = string
  default     = "oci_dg_sample"
  description = "oci dg name"
}

variable compartment_ocid{
    type     = string
    default  = ""
}

variable compartment_name {
    type = string
    default = ""
}

variable region{
    type = string
    default = "us-ashburn-1"
}

variable tenancy_ocid{
    type = string
    default = "ocid1.tenancy.oc1..aaaaaaaasu7rvefmsyk5kqczfmdqi5clpddejfjk2attdqnk6sbk72wajq5q"
}