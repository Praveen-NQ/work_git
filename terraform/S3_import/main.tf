provider "aws" {
  region = "us-east-1"
  profile = "default"
}

resource "aws_s3_bucket" "scripts_bucket" {
  bucket              = "install-scripts1"
  bucket_prefix       = null
  force_destroy       = null
  object_lock_enabled = false
  tags = {
    purpose = "scrpt savings"
  }
  tags_all = {
    purpose = "scrpt savings"
  }
}