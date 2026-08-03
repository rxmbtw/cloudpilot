data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "cloudpilot_server" {

  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  key_name = aws_key_pair.cloudpilot_key.key_name

  subnet_id = aws_subnet.public_subnet_a.id

  vpc_security_group_ids = [
    aws_security_group.cloudpilot_sg.id
  ]

  associate_public_ip_address = true

  user_data = file("${path.module}/../../scripts/user_data.sh")

  user_data_replace_on_change = true

  tags = {
    Name = "cloudpilot-server"
  }
}
