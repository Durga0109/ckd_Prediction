#!/bin/bash

# AWS ECR Configuration
AWS_ACCOUNT_ID="302263040839"
AWS_REGION="ap-south-1"
ECR_REPOSITORY_NAME="ckd-prediction-system"
IMAGE_TAG="latest"

echo "Step 1: Authenticating with Amazon ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

echo "Step 2: Tagging the image for ECR..."
docker tag ckd-prediction-system:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

echo "Step 3: Pushing the image to ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

echo "✅ Image successfully pushed to ECR!"
echo "Repository URI: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest"

