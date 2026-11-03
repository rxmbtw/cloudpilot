resource "aws_security_group" "cloudpilot_sg" {
  name        = "cloudpilot-sg"
  description = "CloudPilot lab - HTTP from my IP only"
  vpc_id      = aws_vpc.cloudpilot_vpc.id

  ingress {
    description = "HTTP from my IP only"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  egress {
    description = "Allow all outbound (pull images, reach SSM)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "cloudpilot-sg"
  }
}
