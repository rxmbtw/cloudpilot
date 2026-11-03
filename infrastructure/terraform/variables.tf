variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "my_ip" {
  description = "Public IP allowed to SSH into EC2"
  type        = string
}
