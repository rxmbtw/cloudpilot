data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  # ARN prefix for this lab's parameters: arn:aws:ssm:<region>:<account>:parameter/cloudpilot/lab
  lab_params_arn = "arn:aws:ssm:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:parameter/cloudpilot/lab"
}

# The badge. The trust policy says: only EC2 servers may wear it.
resource "aws_iam_role" "ec2" {
  name = "cloudpilot-lab-ec2"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# Door 1: read ONLY /cloudpilot/lab/* secrets, and decrypt them only through SSM
resource "aws_iam_role_policy" "read_lab_secrets" {
  name = "read-lab-secrets"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ReadLabParameters"
        Effect   = "Allow"
        Action   = ["ssm:GetParameter", "ssm:GetParameters", "ssm:GetParametersByPath"]
        Resource = [local.lab_params_arn, "${local.lab_params_arn}/*"]
      },
      {
        Sid       = "DecryptViaSsmOnly"
        Effect    = "Allow"
        Action    = "kms:Decrypt"
        Resource  = "*"
        Condition = { StringEquals = { "kms:ViaService" = "ssm.${data.aws_region.current.region}.amazonaws.com" } }
      }
    ]
  })
}

# Door 2: the minimum Session Manager needs (instead of AmazonSSMManagedInstanceCore)
resource "aws_iam_role_policy" "session_manager" {
  name = "session-manager-minimal"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ssm:UpdateInstanceInformation",
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel",
      ]
      Resource = "*"
    }]
  })
}

# The clip that attaches the badge to an EC2 instance
resource "aws_iam_instance_profile" "ec2" {
  name = "cloudpilot-lab-ec2"
  role = aws_iam_role.ec2.name
}
