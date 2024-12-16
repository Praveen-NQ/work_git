provider "aws" {
  region = var.region
  profile = var.profile
  #access_key = var.access_key
  #secret_key = var.secret_key
}

data "aws_s3_object" "user_data" {
  bucket = var.bucket
  key = var.key
}

resource "aws_security_group_rule" "ingress_rules" {
  count = length(var.ingress_rules)
  type              = var.sgr_type  # sgr_type = "ingress"
  security_group_id = var.sgi
  from_port         = var.ingress_rules[count.index].from_port
  to_port           = var.ingress_rules[count.index].to_port
  protocol          = var.ingress_rules[count.index].protocol
  cidr_blocks       = [var.ingress_rules[count.index].cidr_block]
  description       = var.ingress_rules[count.index].description
}

resource "aws_instance" "terraform_saample"  {
  associate_public_ip_address     = true
  count                           = var.number_of_instances
  ami                             = var.ami
  instance_type                   = var.itype
  subnet_id                       = var.subnet
  #security_groups                 = var.securitygroupid
  key_name                        = var.pem_file
  user_data                       = data.aws_s3_object.user_data.body
  iam_instance_profile            = var.iam_instance_profile
    root_block_device {
    delete_on_termination = true
    volume_size = var.vol_size
    volume_type = var.vol_type
  }
  tags = {
    Name =var.tag_name
    Environment = var.tag_env
    OS = var.tag_os
    Managed = var.tag_mgmnt_type
  }
# Login to the ec2-user with the aws key.
connection {
  type        = "ssh"
  user        = "ec2-user"
  private_key = file(var.keyPath)
  host        = self.public_ip
  }
}