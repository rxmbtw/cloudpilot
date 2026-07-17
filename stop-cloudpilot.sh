#!/bin/bash

echo "========================================"
echo "🛑 Stopping CloudPilot"
echo "========================================"

echo ""
echo "▶ Stopping Docker Compose services..."
docker compose down

echo ""
echo "▶ Stopping Minikube..."
minikube stop

echo ""
echo "========================================"
echo "✅ CloudPilot Stopped"
echo "========================================"

echo ""
echo "If the GitHub Runner is running,"
echo "press Ctrl+C in the runner terminal."
