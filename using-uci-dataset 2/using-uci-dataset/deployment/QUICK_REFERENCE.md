# CKD Prediction System Deployment - Quick Reference

This is a quick reference guide for deploying the CKD Prediction System to Kubernetes using Docker and Amazon ECR.

## Prerequisites

- Docker installed and running
- AWS CLI configured with appropriate permissions
- kubectl configured to access your Kubernetes cluster
- AWS Account ID and Region

## Quick Commands

### Docker Build and Push

```bash
# Set your variables
export AWS_ACCOUNT_ID="your-aws-account-id"
export AWS_REGION="your-aws-region"
export ECR_REPOSITORY="ckd-prediction-system"

# Authenticate with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build image
docker build -t $ECR_REPOSITORY:latest -f deployment/Dockerfile .

# Tag image
docker tag $ECR_REPOSITORY:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest

# Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
```

### Kubernetes Deployment

```bash
# Set namespace
export NAMESPACE="default"

# Update image references in deployment.yaml
sed -i.bak "s|\${AWS_ACCOUNT_ID}|$AWS_ACCOUNT_ID|g" deployment/kubernetes/deployment.yaml
sed -i.bak "s|\${AWS_REGION}|$AWS_REGION|g" deployment/kubernetes/deployment.yaml

# Apply manifests
kubectl apply -f deployment/kubernetes/deployment.yaml -n $NAMESPACE
kubectl apply -f deployment/kubernetes/service.yaml -n $NAMESPACE
kubectl apply -f deployment/kubernetes/ingress.yaml -n $NAMESPACE

# Verify deployment
kubectl get pods -n $NAMESPACE -l app=ckd-prediction-system
kubectl get services -n $NAMESPACE -l app=ckd-prediction-system
```

### Access the Application

```bash
# Port forwarding (local access)
kubectl port-forward svc/ckd-prediction-service 8080:80 -n $NAMESPACE

# Get ingress address (external access)
kubectl get ingress ckd-prediction-ingress -n $NAMESPACE
```

## Folder Structure

```
deployment/
├── Dockerfile
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── scripts/
│   ├── build_and_push.sh
│   └── deploy_to_kubernetes.sh
└── README.md
```

## Key Configuration

### Deployment Specs
- **Replicas:** 3
- **Container Port:** 8501
- **Resource Requests:** 512Mi memory, 250m CPU
- **Resource Limits:** 1Gi memory, 500m CPU

### Service Specs
- **Type:** ClusterIP
- **Port:** 80
- **Target Port:** 8501

## Troubleshooting

### Check Pod Status
```bash
kubectl describe pod <pod-name> -n $NAMESPACE
kubectl logs <pod-name> -n $NAMESPACE
```

### Check Service
```bash
kubectl get endpoints -n $NAMESPACE
kubectl describe service ckd-prediction-service -n $NAMESPACE
```

### Restart Deployment
```bash
kubectl rollout restart deployment ckd-prediction-system -n $NAMESPACE
```

## Scaling

```bash
# Scale to 5 replicas
kubectl scale deployment ckd-prediction-system --replicas=5 -n $NAMESPACE
```

For detailed instructions, refer to the [Step-by-Step Guide](./STEP_BY_STEP.md) or [README](./README.md).
