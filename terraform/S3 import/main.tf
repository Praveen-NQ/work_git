provider "aws" {
  region = "us-east-1"
  profile = "default"
}

import {
  id = aws_s3_bucket.install-scripts1

  to = aws_s3_bucket.sample
}