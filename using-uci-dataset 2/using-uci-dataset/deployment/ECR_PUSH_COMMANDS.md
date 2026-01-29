# Commands to Push CKD Prediction Image to ECR

## Your ECR Configuration

- **AWS Account ID**: 302263040839
- **Region**: ap-south-1
- **Repository Name**: ckd-prediction-system (or test2 if you want to use that)
- **Image Tag**: latest

## Step-by-Step Commands

### Step 1: Authenticate with ECR

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 302263040839.dkr.ecr.ap-south-1.amazonaws.com
```

**Note**: Make sure your AWS CLI is configured with valid credentials first:
```bash
aws configure
```

### Step 2: Tag the Image for ECR

```bash
docker tag ckd-prediction-system:latest 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd-prediction-system:latest
```

Or if you want to use the repository name "test2":
```bash
docker tag ckd-prediction-system:latest 302263040839.dkr.ecr.ap-south-1.amazonaws.com/test2:latest
```

### Step 3: Push the Image to ECR

For repository name "ckd-prediction-system":
```bash
docker push 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd-prediction-system:latest
```

Or for repository name "test2":
```bash
docker push 302263040839.dkr.ecr.ap-south-1.amazonaws.com/test2:latest
```

## Complete Command Sequence (Copy-Paste Ready)

If using repository "ckd-prediction-system":
```bash
# Authenticate
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 302263040839.dkr.ecr.ap-south-1.amazonaws.com

# Tag
docker tag ckd-prediction-system:latest 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd-prediction-system:latest

# Push
docker push 302263040839.dkr.ecr.ap-south-1.amazonaws.com/ckd-prediction-system:latest
```

If using repository "test2":
```bash
# Authenticate
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 302263040839.dkr.ecr.ap-south-1.amazonaws.com

# Tag
docker tag ckd-prediction-system:latest 302263040839.dkr.ecr.ap-south-1.amazonaws.com/test2:latest

# Push
docker push 302263040839.dkr.ecr.ap-south-1.amazonaws.com/test2:latest
```

## Create ECR Repository (If Not Exists)

If the repository doesn't exist yet, create it first:

```bash
# For ckd-prediction-system
aws ecr create-repository --repository-name ckd-prediction-system --region ap-south-1

# Or for test2
aws ecr create-repository --repository-name test2 --region ap-south-1
```

## Troubleshooting

### If you get "The security token included in the request is invalid":
1. Make sure AWS CLI is configured:
   ```bash
   aws configure
   ```
2. Verify your credentials:
   ```bash
   aws sts get-caller-identity
   ```

### If you get "RepositoryNotFoundException":
Create the repository first using the commands above.

### Verify the Push
After pushing, verify the image in ECR:
```bash
aws ecr describe-images --repository-name ckd-prediction-system --region ap-south-1
```

## Using the Script

Alternatively, you can use the provided script (make sure to edit it first with your repository name):

```bash
chmod +x deployment/PUSH_TO_ECR.sh
./deployment/PUSH_TO_ECR.sh
```

