#variable file
variable "region" {
  description = "To which region we need to do changes or add the resources we will confrim here"
}

variable "access_key" {
  description = "to login"
}

variable "secret_key" {
  description = "to login"
}

variable "profile" {
  description = "to login"
}

variable "number_of_instances" {
  description = "when we need to bring up few machines at-a-time we can change the count here to that much"
}

variable "instance_name" {
  description = "the name machine will be taken from here"
}

variable "ami" {
  description = "The id of the machine image (AMI) to use for the server."
}

variable "itype" {
  description = "The EBS volume type is defined here ."
}

variable "pem_file" {
  description = "key to login into ec2 instance"
}

variable "keyPath" {
}

variable "subnet" {
  description = "The subnet id of the vpc to use for the server."
}

variable "securitygroupid" {
#  type        = list(string)
#  default = ["ssg-000a5e33f834e1969","sg-000a5e33f834e1969","sg-007f5b42cd9519592","sg-01de2f30fa98ecbe0","sg-05d34759cc6ec9b59"]
  description = "The aws_security_group defined here "
}

variable "ingress_rules" {
}

variable "bucket" {  
}

variable "key" {
}

variable "sgr_type" {
}
variable "sgi" {
}

variable "iam_instance_profile" {
}

variable "vol_size" {
}

variable "vol_type" {
}

variable "tag_name" {
}

variable "tag_env" {
}

variable "tag_os" {
}

variable "tag_mgmnt_type" {
}