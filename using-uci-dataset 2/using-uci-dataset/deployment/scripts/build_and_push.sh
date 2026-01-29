#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration - Replace these with your actual values
AWS_ACCOUNT_ID="your-aws-account-id"
AWS_REGION="your-aws-region"  # e.g., us-west-2
ECR_REPOSITORY_NAME="ckd-prediction-system"
IMAGE_TAG="latest"

# Navigate to the project root directory
cd "$(dirname "$0")/../.."

# Build the Docker image
echo "Building Docker image..."
docker build -t ${ECR_REPOSITORY_NAME}:${IMAGE_TAG} -f deployment/Dockerfile .

# Authenticate Docker to your ECR registry
echo "Authenticating with ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Create the repository if it doesn't exist
echo "Ensuring ECR repository exists..."
aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME} --region ${AWS_REGION} || \
    aws ecr create-repository --repository-name ${ECR_REPOSITORY_NAME} --region ${AWS_REGION}

# Tag the image for ECR
echo "Tagging image for ECR..."
docker tag ${ECR_REPOSITORY_NAME}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}

# Push the image to ECR
echo "Pushing image to ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}

echo "Image successfully built and pushed to ECR!"
echo "Repository: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}"
echo "Tag: ${IMAGE_TAG}"
