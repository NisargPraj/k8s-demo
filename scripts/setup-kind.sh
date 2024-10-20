#!/bin/bash

# Define the cluster configuration
cat <<EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
networking:
  apiServerAddress: "127.0.0.1"
  apiServerPort: 6443
EOF

# Create the cluster using the configuration
kind create cluster --name flaskblog-cluster --config kind-config.yaml

# Load local Docker images into Kind
# This assumes you've already built these images with the appropriate tags
docker pull mongo:latest
kind load docker-image backend-flaskblog:latest --name flaskblog-cluster
kind load docker-image frontend-flaskblog:latest --name flaskblog-cluster
kind load docker-image mongo:latest --name flaskblog-cluster

# Apply the Kubernetes manifests
kubectl apply -f ../k8s/

# Wait for all pods to be in the 'Running' state
echo "Waiting for pods to be in the Running state..."
kubectl wait --for=condition=ready pod --all --timeout=300s

# Set up port forwarding in the background for backend
kubectl port-forward service/backend 5000:5000 &
# Set up port forwarding in the background for frontend
kubectl port-forward service/frontend 80:80 &

echo "Kind cluster setup complete. Services are being port forwarded:"
echo " - Backend: http://localhost:8000"
echo " - Frontend: http://localhost:3000"