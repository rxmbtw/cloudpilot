output "vpc_id" {
  value = aws_vpc.cloudpilot_vpc.id
}

output "public_subnet_a_id" {
  value = aws_subnet.public_subnet_a.id
}

output "public_subnet_b_id" {
  value = aws_subnet.public_subnet_b.id
}

output "internet_gateway_id" {
  value = aws_internet_gateway.cloudpilot_igw.id
}

output "ec2_public_ip" {
  value = aws_instance.cloudpilot_server.public_ip
}

output "ec2_public_dns" {
  value = aws_instance.cloudpilot_server.public_dns
}
