#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration - Replace these with your actual values
AWS_ACCOUNT_ID="your-aws-account-id"
AWS_REGION="your-aws-region"  # e.g., us-west-2
ECR_REPOSITORY_NAME="ckd-prediction-system"
IMAGE_TAG="latest"
KUBERNETES_NAMESPACE="default"  # or your custom namespace

# Navigate to the kubernetes directory
cd "$(dirname "$0")/../kubernetes"

# Create namespace if it doesn't exist
kubectl get namespace ${KUBERNETES_NAMESPACE} || kubectl create namespace ${KUBERNETES_NAMESPACE}

# Update the image reference in the deployment file
sed -i.bak "s|\${AWS_ACCOUNT_ID}|${AWS_ACCOUNT_ID}|g" deployment.yaml
sed -i.bak "s|\${AWS_REGION}|${AWS_REGION}|g" deployment.yaml

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f deployment.yaml -n ${KUBERNETES_NAMESPACE}
kubectl apply -f service.yaml -n ${KUBERNETES_NAMESPACE}
kubectl apply -f ingress.yaml -n ${KUBERNETES_NAMESPACE}

# Clean up backup files
rm -f *.bak

echo "Deployment complete!"
echo "Checking deployment status..."
kubectl get deployments -n ${KUBERNETES_NAMESPACE} | grep ckd-prediction-system
kubectl get services -n ${KUBERNETES_NAMESPACE} | grep ckd-prediction-service
kubectl get ingress -n ${KUBERNETES_NAMESPACE} | grep ckd-prediction-ingress

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=ckd-prediction-system -n ${KUBERNETES_NAMESPACE} --timeout=120s

echo "CKD Prediction System successfully deployed with 3 replicas!"
echo "Access the application through the ingress or use port-forwarding:"
echo "kubectl port-forward svc/ckd-prediction-service 8080:80 -n ${KUBERNETES_NAMESPACE}"
