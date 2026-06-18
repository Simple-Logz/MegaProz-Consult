variable "app_name" { default = "MegaProz-Consult" }
variable "aws_region" { default = "us-east-1" }
variable "db_password" { sensitive = true }
variable "image_tag" { default = "latest" }