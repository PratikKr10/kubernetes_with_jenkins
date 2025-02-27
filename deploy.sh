#!/bin/bash
set -e

echo "🚀 Starting Kubernetes Deployment..."

# Start Minikube
if ! minikube status | grep -q "host: Running"; then
    echo "🔄 Starting Minikube..."
    minikube start
else
    echo "✅ Minikube is already running."
fi

# Use Minikube's Docker environment
eval $(minikube docker-env)

# Build Docker Image
echo "🐳 Building Docker Image..."
cd app
docker build -t my-k8s-app:latest .
cd ..

# Deploy Kubernetes Resources
echo "🛠 Applying Kubernetes resources..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for Deployment
echo "⏳ Waiting for pods to be ready..."
kubectl -n demo-namespace rollout status deployment/flask-app

# Get Service URL
echo "🔗 Application is running! Access it at:"
minikube service flask-service -n demo-namespace --url
