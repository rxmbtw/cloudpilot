resource "aws_key_pair" "cloudpilot_key" {
  key_name   = "cloudpilot-key"
  public_key = file("${path.module}/../../ssh/cloudpilot-key-v2.pub")


  tags = {
    Name = "cloudpilot-key"
  }
}
