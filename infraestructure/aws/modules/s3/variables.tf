variable "bucket" {
  type = string
}

variable "acl" {
  type = string
}

variable "versioning" {
  type = bool
}

variable "subnet_s3" {
  type = list(string)
}

variable "vpc_id_s3" {
  description = "VPC id"
}
