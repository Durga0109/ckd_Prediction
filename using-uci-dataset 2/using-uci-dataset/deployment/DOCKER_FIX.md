# Docker Build Fixes for CKD Prediction System

## Issue Fixed

**Problem**: `Failed to load models: No module named 'numpy._core'`

**Root Cause**: NumPy compatibility issue with Python 3.9 and the numpy version in requirements.txt.

## Solutions Applied

### 1. Updated Python Version
- Changed from `python:3.9-slim` to `python:3.10-slim` for better numpy compatibility

### 2. Improved Dependency Installation
- Upgraded pip, setuptools, and wheel first
- Installed numpy separately before other packages
- This ensures numpy is built correctly

### 3. Updated Requirements
- Changed from pinned versions to flexible version ranges
- Allows pip to resolve compatible versions automatically

### 4. Created .dockerignore
- Ensures model files (.pkl) are included in the Docker image
- Excludes unnecessary files to reduce image size

## Building the Docker Image

### Prerequisites

1. **Ensure models are trained first:**
   ```bash
   python3 train_model.py
   ```
   This creates all necessary `.pkl` files in the project root.

2. **Verify model files exist:**
   ```bash
   ls -la *.pkl
   ```
   You should see:
   - `ckd_best_model.pkl`
   - `ckd_scaler.pkl`
   - `ckd_feature_names.pkl`
   - `ckd_label_encoders.pkl`
   - `ckd_target_encoder.pkl`
   - `ckd_knn_imputer.pkl`
   - `ckd_test_metrics.pkl`

### Build Command

```bash
# Navigate to project root
cd "/Users/jeevanantham/Documents/final year project/using-uci-dataset"

# Build the Docker image
docker build -t ckd-prediction-system:latest .
```

### Test the Docker Image Locally

```bash
# Run the container
docker run -p 8501:8501 ckd-prediction-system:latest

# Access the app at http://localhost:8501
```

## Troubleshooting

### If models are missing in the container:

1. **Check if models exist in your project directory:**
   ```bash
   ls -la *.pkl
   ```

2. **If models don't exist, train them first:**
   ```bash
   python3 train_model.py
   ```

3. **Rebuild the Docker image:**
   ```bash
   docker build -t ckd-prediction-system:latest .
   ```

### If numpy errors persist:

1. **Clear Docker build cache:**
   ```bash
   docker builder prune -a
   ```

2. **Rebuild without cache:**
   ```bash
   docker build --no-cache -t ckd-prediction-system:latest .
   ```

### Verify numpy installation in container:

```bash
# Run an interactive shell in the container
docker run -it --entrypoint /bin/bash ckd-prediction-system:latest

# Inside the container, verify numpy:
python3 -c "import numpy; print(numpy.__version__)"
```

## Updated Dockerfile Structure

```dockerfile
FROM python:3.10-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel first
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt .

# Install numpy first (fixes compatibility issues)
RUN pip install --no-cache-dir numpy>=1.24.3

# Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application (including .pkl model files)
COPY . .

# Expose port and run
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Next Steps

After successfully building the Docker image:

1. Test it locally to ensure it works
2. Push to ECR using the build_and_push.sh script
3. Deploy to Kubernetes using the deployment scripts

## Notes

- **Important**: Always train the models before building the Docker image
- The model files must be in the project root directory
- The `.dockerignore` file ensures model files are included
- Python 3.10 provides better numpy compatibility than Python 3.9
