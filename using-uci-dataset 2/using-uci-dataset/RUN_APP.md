# How to Run the CKD Prediction App

## Quick Start Guide

Follow these steps to run the CKD Prediction System web interface:

### 1. Install Required Packages

First, make sure all required packages are installed:

```bash
pip install -r requirements.txt
```

You might also need to install watchdog for better file monitoring:

```bash
pip install watchdog
```

### 2. Train the Model (if not already done)

If you haven't trained the model yet, run:

```bash
python3 train_model.py
```

This will:
- Process the dataset
- Train the model
- Save all necessary files

### 3. Run the Streamlit App

Start the web interface with:

```bash
streamlit run app.py
```

The app should automatically open in your default web browser at http://localhost:8501

### 4. Using the App

1. **Input Patient Data:**
   - Use the sidebar to enter patient information
   - Or select one of the pre-defined examples

2. **Make Prediction:**
   - Click the "Predict CKD Status" button

3. **View Results:**
   - CKD prediction with probability
   - eGFR value and visualization
   - CKD stage determination
   - Feature importance (SHAP)
   - Clinical recommendations

## Troubleshooting

### Common Issues:

1. **Missing Model Files:**
   - Error: "The following required files are missing"
   - Solution: Run `python3 train_model.py` first

2. **Import Errors:**
   - Error: "No module named X"
   - Solution: Run `pip install -r requirements.txt`

3. **Port Already in Use:**
   - Error: "Address already in use"
   - Solution: Kill the process using that port or use a different port:
     ```bash
     streamlit run app.py --server.port 8502
     ```

4. **Visualization Not Showing:**
   - Issue: SHAP visualization not appearing
   - Solution: Make a prediction first by clicking the "Predict" button

## Additional Information

- The app saves prediction results in `patient_shap_report.png`
- You can modify the app by editing `app.py`
- For more details about the system, see `README.md`
