#!/bin/bash
set -eux

dnf update -y
dnf install docker -y

systemctl enable docker
systemctl start docker

usermod -aG docker ec2-user

sleep 10

docker pull ghcr.io/rxmbtw/cloudpilot-api:main

docker rm -f cloudpilot || true

docker run -d \
  --name cloudpilot \
  --restart unless-stopped \
  -p 8000:8000 \
  ghcr.io/rxmbtw/cloudpilot-api:main
