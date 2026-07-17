#!/bin/bash

echo "========================================"
echo "🚀 Starting CloudPilot Development Environment"
echo "========================================"

echo ""
echo "▶ Starting Minikube..."
minikube start

echo ""
echo "▶ Starting Docker Compose services..."
docker compose up -d

echo ""
echo "▶ Waiting for Kubernetes..."
sleep 5

echo ""
echo "▶ Current Pods"
kubectl get pods

echo ""
echo "▶ Current Services"
kubectl get svc

echo ""
echo "▶ Helm Releases"
helm list

echo ""
echo "▶ HPA"
kubectl get hpa

echo ""
echo "========================================"
echo "✅ CloudPilot is Ready!"
echo "========================================"

echo ""
echo "To start the GitHub Runner:"
echo ""
echo "cd ~/actions-runner"
echo "./run.sh"
