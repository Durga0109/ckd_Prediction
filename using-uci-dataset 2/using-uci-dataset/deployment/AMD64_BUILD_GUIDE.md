# Building Docker Image for AMD64 Architecture

This guide shows you how to build and push the CKD Prediction Docker image for AMD64 architecture (required for most Kubernetes clusters).

## Problem

When building on Apple Silicon (M1/M2/M3) Macs, Docker builds for ARM64 by default. Kubernetes clusters typically run on AMD64 architecture, causing a platform mismatch.

## Solution

Build the Docker image explicitly for `linux/amd64` platform.

## Prerequisites

1. Docker Desktop installed and running
2. AWS CLI configured with credentials
3. ECR repository created (or permission to create one)

## Quick Start - Using the Script

```bash
# Make script executable
chmod +x deployment/BUILD_AND_PUSH_AMD64.sh

# Run the script
./deployment/BUILD_AND_PUSH_AMD64.sh
```

## Manual Steps

### Step 1: Authenticate with AWS ECR

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 302263040839.dkr.ecr.ap-south-1.amazonaws.com
```

**Expected output**: `Login Succeeded`

### Step 2: Create ECR Repository (if not exists)

```bash
aws ecr create-repository --repository-name ckd_prediction --region ap-south-1
```

**Skip this step** if the repository already exists.

### Step 3: Build for AMD64 Platform

**Option A: Using docker buildx (Recommended for multi-arch)**

```bash
# Ensure buildx is available
docker buildx version

# If buildx is not available, install it or use Option B
```

If buildx is available:
```bash
docker buildx build --platform linux/amd64 -t ckd_prediction:latest -f Dockerfile .
```

**Option B: Using docker build --platform (Simpler)**

```bash
docker build --platform linux/amd64 -t ckd_prediction:latest -f Dockerfile .
```

This is the recommended method if buildx is not available.

### Step 4: Tag for ECR

```bash
docker tag ckd_prediction:latest 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd_prediction:latest
```

### Step 5: Push to ECR

```bash
docker push 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd_prediction:latest
```

## Complete Command Sequence (Copy-Paste Ready)

```bash
# Navigate to project directory
cd "/Users/jeevanantham/Documents/final year project/using-uci-dataset"

# Step 1: Authenticate
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 302263040839.dkr.ecr.ap-south-1.amazonaws.com

# Step 2: Create repository (if needed)
aws ecr create-repository --repository-name ckd_prediction --region ap-south-1

# Step 3: Build for AMD64
docker build --platform linux/amd64 -t ckd_prediction:latest -f Dockerfile .

# Step 4: Tag for ECR
docker tag ckd_prediction:latest 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd_prediction:latest

# Step 5: Push to ECR
docker push 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd_prediction:latest
```

## Verify the Image Architecture

After building, verify the image is AMD64:

```bash
# Check local image
docker inspect ckd_prediction:latest | grep Architecture
```

Expected output should show: `"Architecture": "amd64"`

Or check in ECR:

```bash
aws ecr describe-images --repository-name ckd_prediction --region ap-south-1 --image-ids imageTag=latest
```

## Troubleshooting

### Error: "platform is not supported"

If you get this error, Docker Desktop might need to enable emulation:

1. Open Docker Desktop
2. Go to Settings > Features in development
3. Enable "Use containerd for pulling and storing images"
4. Or enable "Use Docker Compose V2"

Alternatively, you can use buildx with QEMU emulation:

```bash
# Set up buildx builder
docker buildx create --name multiarch --use

# Build with emulation
docker buildx build --platform linux/amd64 -t ckd_prediction:latest -f Dockerfile . --load
```

### Error: "no space left on device"

If you're running out of space, clean up Docker:

```bash
# Remove unused images
docker image prune -a

# Or remove all unused resources
docker system prune -a --volumes
```

### Build Takes Too Long

AMD64 builds on ARM machines use emulation, which is slower. This is normal. Expect the build to take 10-20 minutes.

### Verify Platform After Push

```bash
# Describe the image in ECR
aws ecr describe-images \
    --repository-name ckd_prediction \
    --region ap-south-1 \
    --image-ids imageTag=latest \
    --query 'imageDetails[0].imageManifestMediaType'
```

## Update Kubernetes Deployment

After pushing, make sure your `deployment.yaml` uses the correct image:

```yaml
image: 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd_prediction:latest
```

## Notes

- Building for AMD64 on ARM machines uses emulation, so it will be slower
- The final image size might be slightly different
- All dependencies will be compiled for AMD64 architecture
- The image will work on AMD64 Kubernetes nodes

## Performance Tips

1. Build during off-peak hours (emulation is CPU-intensive)
2. Use `--no-cache` only if needed: `docker build --platform linux/amd64 --no-cache ...`
3. Consider using GitHub Actions or AWS CodeBuild for CI/CD (they run on AMD64 natively)

