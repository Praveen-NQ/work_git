provider "aws" {
  region = var.region
  profile = var.profile
}
module "Ec2_app" {
  source = "git::https://github.com/Praveengoud25/work_git.git//terraform/Ec2_module"
}