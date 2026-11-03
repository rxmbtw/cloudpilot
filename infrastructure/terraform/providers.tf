provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "cloudpilot"
      Env       = "lab"
      ManagedBy = "terraform"
    }
  }
}
