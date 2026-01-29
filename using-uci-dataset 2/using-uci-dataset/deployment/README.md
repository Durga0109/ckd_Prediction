# CKD Prediction System Deployment Guide

This guide provides step-by-step instructions for containerizing the CKD Prediction System with Docker, pushing it to Amazon ECR, and deploying it on Kubernetes with 3 replicas and a ClusterIP service.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Step 1: Build and Push Docker Image to ECR](#step-1-build-and-push-docker-image-to-ecr)
4. [Step 2: Deploy to Kubernetes](#step-2-deploy-to-kubernetes)
5. [Step 3: Verify the Deployment](#step-3-verify-the-deployment)
6. [Step 4: Access the Application](#step-4-access-the-application)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following tools installed:

- [Docker](https://docs.docker.com/get-docker/)
- [AWS CLI](https://aws.amazon.com/cli/) (configured with appropriate permissions)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (configured to access your Kubernetes cluster)
- [eksctl](https://eksctl.io/) (if using Amazon EKS)

You'll also need:
- An AWS account with permissions to create and push to ECR repositories
- A Kubernetes cluster (e.g., Amazon EKS, GKE, or a local cluster like Minikube)
- AWS credentials configured (`aws configure`)

## Project Structure

```
deployment/
├── Dockerfile                   # Docker configuration for the application
├── kubernetes/
│   ├── deployment.yaml          # Kubernetes Deployment with 3 replicas
│   ├── service.yaml             # ClusterIP Service configuration
│   └── ingress.yaml             # Optional Ingress for external access
├── scripts/
│   ├── build_and_push.sh        # Script to build and push Docker image to ECR
│   └── deploy_to_kubernetes.sh  # Script to deploy to Kubernetes
└── README.md                    # This documentation
```

## Step 1: Build and Push Docker Image to ECR

### 1.1. Configure AWS CLI

Ensure your AWS CLI is configured with the correct credentials:

```bash
aws configure
```

### 1.2. Update Configuration Variables

Edit the `scripts/build_and_push.sh` file and update the following variables:

```bash
AWS_ACCOUNT_ID="your-aws-account-id"
AWS_REGION="your-aws-region"  # e.g., us-west-2
ECR_REPOSITORY_NAME="ckd-prediction-system"
IMAGE_TAG="latest"
```

### 1.3. Build and Push the Docker Image

Run the build and push script:

```bash
cd /path/to/using-uci-dataset
./deployment/scripts/build_and_push.sh
```

This script will:
1. Build the Docker image using the Dockerfile
2. Authenticate with AWS ECR
3. Create the ECR repository if it doesn't exist
4. Tag the image for ECR
5. Push the image to ECR

### 1.4. Verify the Image in ECR

Check that your image was successfully pushed to ECR:

```bash
aws ecr describe-images --repository-name ckd-prediction-system --region your-aws-region
```

## Step 2: Deploy to Kubernetes

### 2.1. Update Configuration Variables

Edit the `scripts/deploy_to_kubernetes.sh` file and update the following variables:

```bash
AWS_ACCOUNT_ID="your-aws-account-id"
AWS_REGION="your-aws-region"  # e.g., us-west-2
ECR_REPOSITORY_NAME="ckd-prediction-system"
IMAGE_TAG="latest"
KUBERNETES_NAMESPACE="default"  # or your custom namespace
```

### 2.2. Deploy to Kubernetes

Run the deployment script:

```bash
cd /path/to/using-uci-dataset
./deployment/scripts/deploy_to_kubernetes.sh
```

This script will:
1. Create the namespace if it doesn't exist
2. Update the image reference in the deployment file
3. Apply the Kubernetes manifests (deployment, service, ingress)
4. Wait for the pods to be ready

## Step 3: Verify the Deployment

### 3.1. Check Deployment Status

```bash
kubectl get deployments -n default
```

You should see `ckd-prediction-system` with 3/3 replicas available.

### 3.2. Check Pods

```bash
kubectl get pods -n default -l app=ckd-prediction-system
```

You should see 3 pods running.

### 3.3. Check Service

```bash
kubectl get services -n default -l app=ckd-prediction-system
```

You should see `ckd-prediction-service` with type `ClusterIP`.

## Step 4: Access the Application

### 4.1. Using Port Forwarding (for local access)

```bash
kubectl port-forward svc/ckd-prediction-service 8080:80 -n default
```

Then access the application at http://localhost:8080

### 4.2. Using Ingress (for external access)

If you've configured the ingress with a valid domain name and DNS settings:

1. Update the hostname in `kubernetes/ingress.yaml` with your actual domain
2. Access the application at http://your-domain.com

## Troubleshooting

### Common Issues

#### Image Pull Errors

If pods are stuck in `ImagePullBackOff` or `ErrImagePull` state:

1. Check ECR permissions:
```bash
kubectl create secret docker-registry regcred \
  --docker-server=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region ${AWS_REGION}) \
  --namespace=default
```

2. Update the deployment to use the secret:
```yaml
spec:
  template:
    spec:
      imagePullSecrets:
      - name: regcred
```

#### Pod Startup Issues

If pods are failing to start:

```bash
kubectl describe pod <pod-name> -n default
kubectl logs <pod-name> -n default
```

#### Service Connection Issues

If you can't connect to the service:

```bash
kubectl get endpoints -n default
kubectl describe service ckd-prediction-service -n default
```

### Scaling the Deployment

To change the number of replicas:

```bash
kubectl scale deployment ckd-prediction-system --replicas=5 -n default
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
