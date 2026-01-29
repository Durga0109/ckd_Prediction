# How to Run the CKD Prediction System with Streamlit

This guide will help you run the CKD Prediction System using Streamlit web interface.

## Prerequisites

1. **Python 3.9 or higher** installed
2. **All dependencies** installed
3. **Trained model files** (`.pkl` files) in the project directory

## Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd "/Users/jeevanantham/Documents/final year project/using-uci-dataset"

# Install all required packages
pip3 install -r requirements.txt
```

**Or if you prefer using pip:**
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model (If Not Already Done)

**Skip this step if you already have these files:**
- `ckd_best_model.pkl`
- `ckd_scaler.pkl`
- `ckd_feature_names.pkl`
- `ckd_label_encoders.pkl`
- `ckd_target_encoder.pkl`
- `ckd_knn_imputer.pkl`

**If files are missing, run:**
```bash
python3 train_model.py
```

This will take a few minutes to train the model.

### Step 3: Run Streamlit App

```bash
streamlit run app.py
```

**That's it!** The app will automatically:
- Open in your default web browser
- Display at `http://localhost:8501`
- Show the CKD Prediction interface

## Detailed Instructions

### Check if Model Files Exist

```bash
# List all model files
ls -la *.pkl
```

You should see at least these files:
- `ckd_best_model.pkl`
- `ckd_scaler.pkl`
- `ckd_feature_names.pkl`
- `ckd_label_encoders.pkl`
- `ckd_target_encoder.pkl`
- `ckd_knn_imputer.pkl`

### Run the App

```bash
streamlit run app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Access the App

1. **Automatic**: The app should open automatically in your browser
2. **Manual**: If it doesn't open, copy the URL from the terminal and paste it in your browser

## Using the Streamlit App

### 1. Input Patient Data

In the sidebar, you can:

- **Enter values manually** for all 25 clinical parameters:
  - Age, Blood Pressure, Specific Gravity, etc.
  - Lab values (Creatinine, Hemoglobin, etc.)
  - Medical history (Hypertension, Diabetes, etc.)

- **Or select a pre-defined example** from the dropdown:
  - High-Risk CKD Patient
  - Severe CKD Patient
  - Healthy Patient

### 2. Make Prediction

Click the **"Predict CKD Status"** button in the sidebar.

### 3. View Results

The main panel will show:

- **Prediction Result**: CKD or No CKD with probability percentage
- **eGFR Gauge**: Visual representation of kidney function
- **CKD Stage**: Stage 0-5 based on eGFR
- **Clinical Recommendations**: Actionable advice for the patient
- **SHAP Feature Importance**: Top 10 factors influencing the prediction

## Troubleshooting

### Error: "No module named 'streamlit'"

**Solution:**
```bash
pip3 install streamlit
# Or
pip install streamlit
```

### Error: "Failed to load models"

**Solution:** Make sure you've trained the model first:
```bash
python3 train_model.py
```

### Error: "Port 8501 is already in use"

**Solution:** Either:
1. Stop the other Streamlit app running on port 8501
2. Or run on a different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

### App Opens But Shows Errors

**Check:**
1. All model files exist (run `ls -la *.pkl`)
2. Dependencies are installed (run `pip3 list | grep streamlit`)
3. Python version is 3.9+ (run `python3 --version`)

### Browser Doesn't Open Automatically

**Solution:** Manually open:
- `http://localhost:8501` in your browser

## Running on a Different Port

```bash
streamlit run app.py --server.port 8502
```

Then access at: `http://localhost:8502`

## Running on Network (Access from Other Devices)

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from other devices using your computer's IP address:
- `http://YOUR_IP_ADDRESS:8501`

## Stopping the App

Press `Ctrl + C` in the terminal where Streamlit is running.

## Example Workflow

```bash
# 1. Navigate to project
cd "/Users/jeevanantham/Documents/final year project/using-uci-dataset"

# 2. Check if models exist
ls *.pkl

# 3. If models don't exist, train them
python3 train_model.py

# 4. Run Streamlit
streamlit run app.py

# 5. Open browser to http://localhost:8501
# 6. Enter patient data and click "Predict"
# 7. View results!
```

## Additional Streamlit Commands

### View Streamlit Config

```bash
streamlit config show
```

### Clear Streamlit Cache

```bash
streamlit cache clear
```

### Run with Debug Mode

```bash
streamlit run app.py --logger.level=debug
```

## Next Steps

After running the app:

1. **Test with Example Patients**: Use the pre-defined examples to see how it works
2. **Try Your Own Data**: Enter real patient data (anonymized) to test predictions
3. **Review SHAP Explanations**: Understand which features are most important
4. **Check Recommendations**: See what clinical advice is provided

## Need Help?

- Check `STREAMLIT_README.md` for more details
- Review `README.md` for project overview
- See `QUICKSTART.md` for quick reference

## Summary

**To run the app, just 3 commands:**

```bash
pip3 install -r requirements.txt
python3 train_model.py  # Only if models don't exist
streamlit run app.py
```

Then open `http://localhost:8501` in your browser! 🚀

