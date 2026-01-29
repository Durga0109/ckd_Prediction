# Quick Reference: Build and Push for AMD64

## All Commands (Copy-Paste Ready)

```bash
# Navigate to project root
cd "/Users/jeevanantham/Documents/final year project/using-uci-dataset"

# 1. Authenticate with ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 302263040839.dkr.ecr.ap-south-1.amazonaws.com

# 2. Create repository (if doesn't exist)
aws ecr create-repository --repository-name ckd_prediction --region ap-south-1 2>/dev/null || echo "Repository exists"

# 3. Build for AMD64 platform
docker build --platform linux/amd64 -t ckd_prediction:latest -f Dockerfile .

# 4. Tag for ECR
docker tag ckd_prediction:latest 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd_prediction:latest

# 5. Push to ECR
docker push 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd_prediction:latest
```

## Or Use the Script

```bash
./deployment/BUILD_AND_PUSH_AMD64.sh
```

## Verify After Push

```bash
# Check image in ECR
aws ecr describe-images --repository-name ckd_prediction --region ap-south-1 --image-ids imageTag=latest
```

## Important Notes

- ⚠️ **Key**: Use `--platform linux/amd64` to build for AMD64 architecture
- ⏱️ Build will take 10-20 minutes (emulation is slower)
- ✅ Image will work on AMD64 Kubernetes nodes
- 📍 Repository: `ckd_prediction`
- 🌍 Region: `ap-south-1`

