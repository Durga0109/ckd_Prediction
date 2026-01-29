# 🏥 CKD Prediction System - Streamlit Web Interface

This is a web-based interface for the Chronic Kidney Disease (CKD) Prediction System, built with Streamlit.

## 🚀 Getting Started

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Train the Model (if not already done)

```bash
python3 train_model.py
```

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## 📊 Features

- **User-friendly Interface:** Easy-to-use web interface for inputting patient data
- **Interactive Controls:** Sliders and dropdown menus for all 25 clinical parameters
- **Example Patients:** Pre-defined examples for quick testing
- **Visual Results:** 
  - CKD prediction with probability
  - eGFR gauge visualization
  - CKD stage determination
  - SHAP feature importance visualization
  - Clinical recommendations

## 👨‍💻 Usage

1. **Input Patient Data:**
   - Enter values in the sidebar
   - Or select one of the pre-defined examples

2. **Make Prediction:**
   - Click the "Predict CKD Status" button

3. **View Results:**
   - CKD prediction and probability
   - eGFR value and CKD stage
   - Feature importance visualization
   - Clinical recommendations

## 📱 Screenshots

When you run the app, you'll see:

1. A sidebar for entering patient data
2. A main panel showing prediction results
3. Visualizations of eGFR and feature importance
4. Clinical recommendations based on CKD stage

## ⚠️ Medical Disclaimer

This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical diagnosis and treatment decisions.

## 🔍 Technical Details

The Streamlit app is built on top of the core CKD prediction system and provides a user-friendly interface to:

- Load the trained models
- Input patient data
- Run the prediction pipeline
- Visualize results
- Generate clinical recommendations

## 🧪 Example Patients

The app includes three pre-defined example patients:

1. **High-Risk CKD:** 48-year-old male with diabetes and hypertension
2. **Severe CKD:** 62-year-old female with multiple comorbidities
3. **Healthy Patient:** 35-year-old female with no comorbidities

## 🔧 Customization

You can customize the app by:

- Editing the CSS styles in the `streamlit_app.py` file
- Adding more example patients
- Extending the visualization options
- Adding additional tabs or features

## 📚 Learn More

For more information about the CKD prediction system, see:
- `README.md` - Main documentation
- `QUICKSTART.md` - Quick start guide
