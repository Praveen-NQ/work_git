region = "us-east-1"
profile = "default"
number_of_instances = 1
instance_name = "module test"
ami = "ami-0453ec754f44f9a4a"
itype = "t2.micro"
pem_file = "test-vir"
keyPath = "E:/2024/test-vir.pem"
subnet = "subnet-003fd9896f3147027"
securitygroupid = ["ssg-000a5e33f834e1969","sg-000a5e33f834e1969","sg-007f5b42cd9519592","sg-01de2f30fa98ecbe0","sg-05d34759cc6ec9b59"]
bucket = "install-scripts1"
key = "cron_kill.sh"
sgr_type = "ingress"
sgi = "sg-041e18817f5cc6811"
iam_instance_profile= "allows3"
vol_size = 50
vol_type = "gp2"

#tags
tag_name = "SERVER01"
tag_env = "DEV"
tag_mgmnt_type = "IAC"
tag_os = "AL2"

#ec2_login


ingress_rules = [
  {
    protocol    = "tcp"
    from_port   = 0
    to_port     = 65535
    cidr_block  = "0.0.0.0/0"
    description = "opens all ports for incoming"
  },
  {
    protocol    = "udp"
    from_port   = 0
    to_port     = 65535
    cidr_block  = "0.0.0.0/0"
    description = ""
  },
  {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_block  = "0.0.0.0/0"
    description = "test"
  },
  {
    protocol    = "tcp"
    from_port   = 23
    to_port     = 23
    cidr_block  = "0.0.0.0/0"
    description = "test"
  },
  {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_block  = "0.0.0.0/0"
    description = "test"
  },
  {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_block  = "0.0.0.0/0"
    description = "test"
  }
]
