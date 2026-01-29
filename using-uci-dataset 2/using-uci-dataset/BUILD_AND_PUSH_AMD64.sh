#!/bin/bash

# AWS ECR Configuration
AWS_ACCOUNT_ID="302263040839"
AWS_REGION="us-east-1"
ECR_REPOSITORY_NAME="ckd_prediction"
IMAGE_TAG="latest"
PLATFORM="linux/amd64"

echo "=========================================="
echo "Building and Pushing CKD Prediction Image"
echo "=========================================="
echo "Repository: ${ECR_REPOSITORY_NAME}"
echo "Region: ${AWS_REGION}"
echo "Platform: ${PLATFORM}"
echo "=========================================="

# Step 1: Authenticate with ECR
echo ""
echo "Step 1: Authenticating with Amazon ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

if [ $? -ne 0 ]; then
    echo "❌ Authentication failed. Please check your AWS credentials."
    exit 1
fi

echo "✅ Authentication successful!"

# Step 2: Create repository if it doesn't exist
echo ""
echo "Step 2: Ensuring ECR repository exists..."
aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME} --region ${AWS_REGION} > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Creating repository ${ECR_REPOSITORY_NAME}..."
    aws ecr create-repository --repository-name ${ECR_REPOSITORY_NAME} --region ${AWS_REGION}
    echo "✅ Repository created!"
else
    echo "✅ Repository already exists!"
fi

# Step 3: Build for AMD64 platform
echo ""
echo "Step 3: Building Docker image for AMD64 platform..."
docker buildx build --platform ${PLATFORM} -t ${ECR_REPOSITORY_NAME}:${IMAGE_TAG} -f Dockerfile .

if [ $? -ne 0 ]; then
    echo "❌ Build failed. Trying alternative method..."
    echo "Building with docker build --platform..."
    docker build --platform ${PLATFORM} -t ${ECR_REPOSITORY_NAME}:${IMAGE_TAG} -f Dockerfile .
    
    if [ $? -ne 0 ]; then
        echo "❌ Build failed. Please check the Dockerfile and dependencies."
        exit 1
    fi
fi

echo "✅ Image built successfully!"

# Step 4: Tag for ECR
echo ""
echo "Step 4: Tagging image for ECR..."
docker tag ${ECR_REPOSITORY_NAME}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}

echo "✅ Image tagged!"

# Step 5: Push to ECR
echo ""
echo "Step 5: Pushing image to ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}

if [ $? -ne 0 ]; then
    echo "❌ Push failed. Please check your permissions and network connection."
    exit 1
fi

echo "✅ Image successfully pushed to ECR!"
echo ""
echo "=========================================="
echo "Repository URI:"
echo "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:${IMAGE_TAG}"
echo "=========================================="

