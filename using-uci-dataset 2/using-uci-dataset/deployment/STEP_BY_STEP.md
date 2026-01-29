# Step-by-Step Guide: Deploying CKD Prediction System to Kubernetes

This guide provides detailed, step-by-step instructions for containerizing your CKD Prediction System with Docker, pushing it to Amazon ECR, and deploying it on Kubernetes with 3 replicas and a ClusterIP service.

## Step 1: Prepare Your Environment

### Install Required Tools

1. **Install Docker**
   ```bash
   # For macOS (using Homebrew)
   brew install docker
   
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker.io
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   ```

2. **Install AWS CLI**
   ```bash
   # For macOS (using Homebrew)
   brew install awscli
   
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install awscli
   ```

3. **Install kubectl**
   ```bash
   # For macOS (using Homebrew)
   brew install kubectl
   
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y apt-transport-https
   curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
   echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
   sudo apt-get update
   sudo apt-get install -y kubectl
   ```

4. **Configure AWS CLI**
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, region, and output format
   ```

## Step 2: Containerize Your Application

### Create a Dockerfile

1. **Navigate to your project directory**
   ```bash
   cd "/Users/jeevanantham/Documents/final year project/using-uci-dataset"
   ```

2. **Review the Dockerfile**
   The Dockerfile is already created at `deployment/Dockerfile`. It:
   - Uses Python 3.9 as the base image
   - Installs required dependencies
   - Copies your application code
   - Exposes port 8501 for Streamlit
   - Sets up a health check
   - Configures the startup command

## Step 3: Build and Push Docker Image to ECR

### Create an ECR Repository

1. **Create an ECR repository**
   ```bash
   export AWS_REGION="your-aws-region"  # e.g., us-east-1
   export ECR_REPOSITORY_NAME="ckd-prediction-system"
   
   aws ecr create-repository \
       --repository-name $ECR_REPOSITORY_NAME \
       --region $AWS_REGION
   ```

### Build and Push the Docker Image

1. **Get your AWS Account ID**
   ```bash
   export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
   ```

2. **Build the Docker image**
   ```bash
   docker build -t $ECR_REPOSITORY_NAME:latest -f deployment/Dockerfile .
   ```

3. **Authenticate Docker to ECR**
   ```bash
   aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
   ```

4. **Tag the image for ECR**
   ```bash
   docker tag $ECR_REPOSITORY_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest
   ```

5. **Push the image to ECR**
   ```bash
   docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME:latest
   ```

6. **Verify the image in ECR**
   ```bash
   aws ecr describe-images --repository-name $ECR_REPOSITORY_NAME --region $AWS_REGION
   ```

## Step 4: Prepare Kubernetes Manifests

### Update Kubernetes Manifest Files

1. **Update the deployment.yaml file**
   ```bash
   sed -i.bak "s|\${AWS_ACCOUNT_ID}|$AWS_ACCOUNT_ID|g" deployment/kubernetes/deployment.yaml
   sed -i.bak "s|\${AWS_REGION}|$AWS_REGION|g" deployment/kubernetes/deployment.yaml
   ```

## Step 5: Deploy to Kubernetes

### Create a Namespace (Optional)

1. **Create a namespace for your application**
   ```bash
   export KUBERNETES_NAMESPACE="ckd-system"
   kubectl create namespace $KUBERNETES_NAMESPACE
   ```

### Apply Kubernetes Manifests

1. **Deploy the application**
   ```bash
   kubectl apply -f deployment/kubernetes/deployment.yaml -n $KUBERNETES_NAMESPACE
   ```

2. **Create the ClusterIP service**
   ```bash
   kubectl apply -f deployment/kubernetes/service.yaml -n $KUBERNETES_NAMESPACE
   ```

3. **Apply the ingress (optional, for external access)**
   ```bash
   kubectl apply -f deployment/kubernetes/ingress.yaml -n $KUBERNETES_NAMESPACE
   ```

## Step 6: Verify the Deployment

### Check Deployment Status

1. **Check the deployment status**
   ```bash
   kubectl get deployments -n $KUBERNETES_NAMESPACE
   ```
   You should see 3/3 replicas available for `ckd-prediction-system`.

2. **Check the pods**
   ```bash
   kubectl get pods -n $KUBERNETES_NAMESPACE -l app=ckd-prediction-system
   ```
   You should see 3 pods in the `Running` state.

3. **Check the service**
   ```bash
   kubectl get services -n $KUBERNETES_NAMESPACE
   ```
   You should see `ckd-prediction-service` with type `ClusterIP`.

## Step 7: Access the Application

### Access Using Port Forwarding

1. **Use port forwarding to access the application locally**
   ```bash
   kubectl port-forward svc/ckd-prediction-service 8080:80 -n $KUBERNETES_NAMESPACE
   ```

2. **Open the application in your browser**
   Visit http://localhost:8080

### Access Using Ingress (If Configured)

1. **Get the ingress address**
   ```bash
   kubectl get ingress -n $KUBERNETES_NAMESPACE
   ```

2. **Access the application using the ingress address**
   Visit the address shown in the output.

## Step 8: Scaling and Management

### Scale the Deployment

1. **Scale the deployment to more replicas if needed**
   ```bash
   kubectl scale deployment ckd-prediction-system --replicas=5 -n $KUBERNETES_NAMESPACE
   ```

### Monitor the Deployment

1. **Monitor pod resource usage**
   ```bash
   kubectl top pods -n $KUBERNETES_NAMESPACE
   ```

2. **View pod logs**
   ```bash
   # Replace pod-name with an actual pod name
   kubectl logs pod-name -n $KUBERNETES_NAMESPACE
   ```

## Step 9: Clean Up (When Needed)

### Delete Kubernetes Resources

1. **Delete the deployment, service, and ingress**
   ```bash
   kubectl delete -f deployment/kubernetes/deployment.yaml -n $KUBERNETES_NAMESPACE
   kubectl delete -f deployment/kubernetes/service.yaml -n $KUBERNETES_NAMESPACE
   kubectl delete -f deployment/kubernetes/ingress.yaml -n $KUBERNETES_NAMESPACE
   ```

2. **Delete the namespace (if created)**
   ```bash
   kubectl delete namespace $KUBERNETES_NAMESPACE
   ```

### Clean Up ECR Resources

1. **Delete the ECR repository**
   ```bash
   aws ecr delete-repository --repository-name $ECR_REPOSITORY_NAME --force --region $AWS_REGION
   ```

## Automation Scripts

For convenience, you can use the provided scripts:

1. **Build and push to ECR**
   ```bash
   # Update variables in the script first
   ./deployment/scripts/build_and_push.sh
   ```

2. **Deploy to Kubernetes**
   ```bash
   # Update variables in the script first
   ./deployment/scripts/deploy_to_kubernetes.sh
   ```

## Troubleshooting

### Common Issues and Solutions

1. **Image Pull Errors**
   ```bash
   # Check pod status
   kubectl describe pod <pod-name> -n $KUBERNETES_NAMESPACE
   
   # Create ECR pull secret if needed
   kubectl create secret docker-registry regcred \
     --docker-server=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com \
     --docker-username=AWS \
     --docker-password=$(aws ecr get-login-password --region $AWS_REGION) \
     --namespace=$KUBERNETES_NAMESPACE
   ```

2. **Pod Startup Issues**
   ```bash
   # Check pod logs
   kubectl logs <pod-name> -n $KUBERNETES_NAMESPACE
   ```

3. **Service Connection Issues**
   ```bash
   # Check service endpoints
   kubectl get endpoints -n $KUBERNETES_NAMESPACE
   ```

## Conclusion

You have successfully:
1. Containerized your CKD Prediction System
2. Pushed the container image to Amazon ECR
3. Deployed the application to Kubernetes with 3 replicas
4. Created a ClusterIP service for internal communication
5. (Optionally) Set up an ingress for external access

Your application is now running in a scalable, containerized environment with proper Kubernetes resource management.
