//
provider "aws" {
  region = "us-east-1"
  profile = "default"
}

import {
  id = "install-scripts1"               //Resource name

  to = aws_s3_bucket.scripts_bucket     //Resource type and conical name
}

//arn:aws:s3:::install-scripts1  // bucket name

//terraform plan -generate-config-out="main.tf" // create a main.tf file from other config file
//terraform import -config=main.tf aws_s3_bucket.scripts_bucket install-scripts1  // using main.tf create statefile for the bucket 


//terraform import aws_s3_bucket.scripts_bucket install-scripts1

//terraform apply -auto-approve

//