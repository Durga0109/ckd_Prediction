"""
CKD Prediction System with Stage Determination and SHAP Explanations

Complete pipeline for Chronic Kidney Disease prediction including:
1. Binary CKD classification with probability
2. CKD stage determination based on eGFR calculation
3. SHAP-based feature importance explanation
4. Clinical recommendations

Author: AI Assistant
Date: October 28, 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib
import warnings
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import xgboost as xgb

warnings.filterwarnings('ignore')
np.random.seed(42)


def load_and_preprocess_data(filepath='chronic_kidney_disease_dataset.csv'):
    """
    Complete data preprocessing pipeline
    
    Tasks:
    1. Load dataset
    2. Clean column names (remove quotes)  
    3. Handle missing values ('?' → NaN)
    4. Convert data types
    5. Encode categorical features
    6. Clean target variable
    7. Handle class imbalance with SMOTE
    8. Scale numerical features
    9. Split data (60% train, 20% validation, 20% test)
    
    Returns:
    - X_train, X_val, X_test, y_train, y_val, y_test
    - scaler, label_encoders, target_encoder, feature_names
    """
    
    print("\n" + "="*80)
    print("📊 DATA PREPROCESSING PIPELINE")
    print("="*80)
    
    # Load data
    print("\n1. Loading dataset...")
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip("'")  # Remove quotes from column names
    print(f"   ✅ Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
    
    # Replace '?' with NaN
    print("\n2. Handling missing values...")
    df = df.replace('?', np.nan)
    missing_counts = df.isnull().sum()
    print(f"   Missing values per feature:")
    for col in missing_counts[missing_counts > 0].index:
        pct = (missing_counts[col] / len(df)) * 100
        print(f"   - {col}: {missing_counts[col]} ({pct:.1f}%)")
    
    # Clean target variable
    df['class'] = df['class'].str.strip()  # Remove whitespace
    df['class'] = df['class'].replace({'no': 'notckd', 'ckd\t': 'ckd'})  # Standardize
    
    print(f"\n3. Target variable distribution:")
    print(f"   {df['class'].value_counts()}")
    
    # Separate features and target
    feature_names = [col for col in df.columns if col != 'class']
    X = df[feature_names].copy()
    y = df['class'].copy()
    
    # Define feature types
    numerical_features = ['age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 
                         'sod', 'pot', 'hemo', 'pcv', 'wbcc', 'rbcc']
    categorical_features = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 
                           'appet', 'pe', 'ane']
    
    # Convert numerical features to float
    print("\n4. Converting data types...")
    for col in numerical_features:
        X[col] = pd.to_numeric(X[col], errors='coerce')
    
    # Handle missing values
    print("\n5. Imputing missing values...")
    # KNN imputation for numerical features
    knn_imputer = KNNImputer(n_neighbors=5)
    X[numerical_features] = knn_imputer.fit_transform(X[numerical_features])
    print(f"   ✅ Numerical features: KNN imputation (k=5)")
    
    # Mode imputation for categorical features
    for col in categorical_features:
        mode_value = X[col].mode()
        if len(mode_value) > 0:
            X[col].fillna(mode_value[0], inplace=True)
    print(f"   ✅ Categorical features: Mode imputation")
    
    # Encode categorical features
    print("\n6. Encoding categorical features...")
    label_encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        print(f"   - {col}: {list(le.classes_)}")
    
    # Encode target variable
    target_encoder = LabelEncoder()
    y = target_encoder.fit_transform(y)  # ckd=0, notckd=1
    print(f"\n7. Target encoding: {dict(zip(target_encoder.classes_, target_encoder.transform(target_encoder.classes_)))}")
    
    # Split data
    print("\n8. Splitting data...")
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, 
                                                      stratify=y, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, 
                                                      stratify=y_temp, random_state=42)
    
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Validation set: {X_val.shape[0]} samples")
    print(f"   Test set: {X_test.shape[0]} samples")
    
    # Scale features
    print("\n9. Scaling features (RobustScaler)...")
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrames
    X_train = pd.DataFrame(X_train_scaled, columns=feature_names)
    X_val = pd.DataFrame(X_val_scaled, columns=feature_names)
    X_test = pd.DataFrame(X_test_scaled, columns=feature_names)
    
    # Apply SMOTE to training data only
    print("\n10. Applying SMOTE to balance training data...")
    print(f"    Before SMOTE: {pd.Series(y_train).value_counts().to_dict()}")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    print(f"    After SMOTE: {pd.Series(y_train_resampled).value_counts().to_dict()}")
    
    print("\n✅ Preprocessing complete!")
    print("="*80)
    
    return (X_train_resampled, X_val, X_test, y_train_resampled, y_val, y_test, 
            scaler, label_encoders, target_encoder, feature_names, knn_imputer)


def train_best_model(X_train, y_train, X_val, y_val):
    """
    Train and select best model using cross-validation
    
    Models to train:
    1. XGBoost (primary)
    2. Random Forest (backup)
    
    Returns:
    - best_model: trained model with highest ROC-AUC
    - model_name: name of best model
    """
    
    print("\n" + "="*80)
    print("🤖 MODEL TRAINING")
    print("="*80)
    
    models = {}
    
    # XGBoost
    print("\n1. Training XGBoost...")
    xgb_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 4, 5, 6],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0]
    }
    
    xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss', use_label_encoder=False)
    xgb_grid = GridSearchCV(xgb_model, xgb_params, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    xgb_grid.fit(X_train, y_train)
    
    # Evaluate on validation set
    xgb_val_pred = xgb_grid.best_estimator_.predict(X_val)
    xgb_val_proba = xgb_grid.best_estimator_.predict_proba(X_val)[:, 1]
    xgb_val_score = roc_auc_score(y_val, xgb_val_proba)
    
    models['XGBoost'] = (xgb_grid.best_estimator_, xgb_grid.best_score_, xgb_val_score)
    print(f"   ✅ XGBoost - CV Score: {xgb_grid.best_score_:.4f}, Val Score: {xgb_val_score:.4f}")
    print(f"   Best params: {xgb_grid.best_params_}")
    
    # Random Forest
    print("\n2. Training Random Forest...")
    rf_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf_model = RandomForestClassifier(random_state=42, n_jobs=-1)
    rf_grid = GridSearchCV(rf_model, rf_params, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    rf_grid.fit(X_train, y_train)
    
    # Evaluate on validation set
    rf_val_pred = rf_grid.best_estimator_.predict(X_val)
    rf_val_proba = rf_grid.best_estimator_.predict_proba(X_val)[:, 1]
    rf_val_score = roc_auc_score(y_val, rf_val_proba)
    
    models['Random Forest'] = (rf_grid.best_estimator_, rf_grid.best_score_, rf_val_score)
    print(f"   ✅ Random Forest - CV Score: {rf_grid.best_score_:.4f}, Val Score: {rf_val_score:.4f}")
    print(f"   Best params: {rf_grid.best_params_}")
    
    # Select best model based on validation score
    best_model_name = max(models.keys(), key=lambda k: models[k][2])
    best_model = models[best_model_name][0]
    
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Cross-validation ROC-AUC: {models[best_model_name][1]:.4f}")
    print(f"   Validation ROC-AUC: {models[best_model_name][2]:.4f}")
    
    print("\n" + "="*80)
    
    return best_model, best_model_name


def evaluate_model(model, X_test, y_test, target_encoder):
    """
    Comprehensive model evaluation on test set
    """
    
    print("\n" + "="*80)
    print("📈 MODEL EVALUATION ON TEST SET")
    print("="*80)
    
    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    
    print(f"\n📊 Performance Metrics:")
    print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1-Score:  {f1:.4f}")
    print(f"   ROC-AUC:   {roc_auc:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n📊 Confusion Matrix:")
    print(f"   {cm}")
    
    # Classification Report
    print(f"\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))
    
    print("="*80)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm
    }


def calculate_egfr(age, sex, creatinine):
    """
    Calculate eGFR using CKD-EPI 2021 equation (race-free)
    
    Formula:
    eGFR = 142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^-1.200 × 0.9938^age × [1.012 if female]
    
    Parameters:
    - age: Patient age in years (float)
    - sex: 'male' or 'female' (string)
    - creatinine: Serum creatinine in mg/dL (float)
    
    Returns:
    - eGFR in mL/min/1.73m² (float)
    """
    
    # Parameters based on sex
    if str(sex).lower() == 'female':
        kappa = 0.7
        alpha = -0.241
        female_factor = 1.012
    else:  # male
        kappa = 0.9
        alpha = -0.302
        female_factor = 1.0
    
    # Calculate eGFR
    min_term = min(creatinine / kappa, 1.0) ** alpha
    max_term = max(creatinine / kappa, 1.0) ** (-1.200)
    age_term = 0.9938 ** age
    
    egfr = 142 * min_term * max_term * age_term * female_factor
    
    return round(egfr, 1)


def determine_ckd_stage(egfr):
    """
    Determine CKD stage based on eGFR (KDIGO 2024 guidelines)
    
    Parameters:
    - egfr: Estimated GFR in mL/min/1.73m² (float)
    
    Returns:
    - stage: Stage number (0-5)
    - description: Stage description (string)
    """
    
    if egfr >= 90:
        return 1, "Stage 1 (G1): Normal or high kidney function"
    elif egfr >= 60:
        return 2, "Stage 2 (G2): Mildly decreased kidney function"
    elif egfr >= 45:
        return 3, "Stage 3a (G3a): Mild to moderately decreased kidney function"
    elif egfr >= 30:
        return 3, "Stage 3b (G3b): Moderately to severely decreased kidney function"
    elif egfr >= 15:
        return 4, "Stage 4 (G4): Severely decreased kidney function"
    else:
        return 5, "Stage 5 (G5): Kidney failure (end-stage)"


def predict_ckd_with_stage(patient_data, model, scaler, feature_names, label_encoders):
    """
    Complete prediction pipeline for single patient
    
    Input:
    - patient_data: dict with all 25 parameters (24 clinical + sex)
    - model: trained ML model
    - scaler: fitted scaler
    - feature_names: list of feature names
    - label_encoders: dict of label encoders
    
    Output:
    - Dictionary with complete results
    """
    
    # Validate input
    required_features = feature_names + ['sex']
    missing_features = [f for f in required_features if f not in patient_data]
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    # Create a copy and encode categorical features
    patient_data_encoded = patient_data.copy()
    
    # Encode categorical features
    categorical_features = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']
    for col in categorical_features:
        if col in label_encoders and col in patient_data_encoded:
            # Convert to string and encode
            value = str(patient_data_encoded[col]).lower()
            try:
                patient_data_encoded[col] = label_encoders[col].transform([value])[0]
            except ValueError:
                # If value not in training set, use most common class
                patient_data_encoded[col] = 0
    
    # Extract clinical features for prediction
    clinical_features = [patient_data_encoded[f] for f in feature_names]
    
    # Scale features
    features_scaled = scaler.transform([clinical_features])
    
    # Get model prediction
    prediction_prob = model.predict_proba(features_scaled)[0]
    prediction_binary = model.predict(features_scaled)[0]
    
    # Determine CKD status (0=ckd, 1=notckd based on target_encoder)
    ckd_status = "CKD" if prediction_binary == 0 else "No CKD"
    ckd_probability = prediction_prob[0] * 100  # Probability of CKD (class 0)
    no_ckd_probability = prediction_prob[1] * 100  # Probability of No CKD (class 1)
    
    # Calculate confidence
    confidence_score = abs(prediction_prob[0] - 0.5) * 2
    if confidence_score >= 0.4:
        confidence = "High"
    elif confidence_score >= 0.2:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    # Determine risk level
    if ckd_probability >= 70:
        risk_level = "High"
    elif ckd_probability >= 50:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Calculate eGFR
    egfr = calculate_egfr(
        age=patient_data['age'],
        sex=patient_data['sex'],
        creatinine=patient_data['sc']
    )
    
    # Determine CKD stage
    if prediction_binary == 0:  # CKD predicted
        stage, stage_description = determine_ckd_stage(egfr)
    else:  # No CKD
        stage = 0
        stage_description = "No CKD - Normal kidney function"
    
    # Generate recommendations
    recommendations = []
    
    # Get probability for more accurate recommendations
    ckd_probability = prediction_prob[0] * 100  # CKD probability
    
    # For very high probability cases, adjust recommendations regardless of eGFR
    if prediction_binary == 0 and ckd_probability >= 95:  # CKD with very high probability
        recommendations.extend([
            "🚨 URGENT: Immediate nephrology consultation required",
            "🏥 Consider hospital admission for comprehensive evaluation",
            "📊 Daily blood pressure monitoring",
            "🥗 Strict renal diet (very low sodium, low protein, low potassium)",
            "💊 Complete medication review for nephrotoxicity",
            "🔬 Weekly kidney function monitoring initially",
            "💧 Careful fluid management (may need restriction)"
        ])
    elif prediction_binary == 0 and ckd_probability >= 90:  # CKD with high probability
        recommendations.extend([
            "⚠️ Urgent nephrology referral (within 1-2 weeks)",
            "📊 Monitor blood pressure 2-3 times daily",
            "🥗 Strict kidney-friendly diet (low sodium, controlled protein)",
            "💧 Careful hydration monitoring",
            "💊 Avoid all NSAIDs and nephrotoxic medications",
            "🔬 Kidney function monitoring every 4-6 weeks"
        ])
    elif stage >= 4:  # Stage 4-5
        recommendations.extend([
            "⚠️ Immediate nephrology consultation",
            "🏥 Prepare for possible renal replacement therapy",
            "📊 Daily blood pressure monitoring",
            "🥗 Very strict kidney-friendly diet",
            "💧 Careful fluid management",
            "💊 Avoid all nephrotoxic medications",
            "🔬 Frequent kidney function monitoring (every 2-4 weeks)"
        ])
    elif stage == 3:  # Stage 3
        recommendations.extend([
            "⚠️ Consult a nephrologist within 1 month",
            "📊 Monitor blood pressure regularly",
            "🥗 Follow a kidney-friendly diet (low sodium, controlled protein)",
            "💧 Stay well hydrated",
            "💊 Avoid NSAIDs and nephrotoxic medications",
            "🔬 Regular monitoring of kidney function every 3 months"
        ])
    elif stage > 0:  # Stage 1-2
        recommendations.extend([
            "👨‍⚕️ Regular check-ups with primary care physician",
            "🔬 Kidney function monitoring every 6-12 months",
            "❤️ Maintain healthy blood pressure and blood sugar",
            "🏃 Stay active and maintain healthy weight",
            "💧 Stay well hydrated"
        ])
    else:  # Stage 0 (No CKD)
        recommendations.extend([
            "✅ Continue healthy lifestyle habits",
            "🏥 Regular health check-ups",
            "⚠️ Manage risk factors (hypertension, diabetes)",
            "💧 Stay hydrated",
            "🏃 Regular exercise"
        ])
    
    # Add diabetes and hypertension recommendations for all CKD cases
    if prediction_binary == 0:  # If CKD predicted
        # Check for diabetes
        dm_value = patient_data.get('dm')
        if dm_value == 'yes' or dm_value == 1:
            recommendations.append("💉 Control diabetes strictly (HbA1c target <7%)")
        
        # Check for hypertension
        htn_value = patient_data.get('htn')
        if htn_value == 'yes' or htn_value == 1:
            recommendations.append("🩺 Strict blood pressure control (<130/80 mmHg)")
    
    return {
        'prediction': ckd_status,
        'ckd_probability': round(ckd_probability, 2),
        'no_ckd_probability': round(no_ckd_probability, 2),
        'confidence': confidence,
        'risk_level': risk_level,
        'egfr': egfr,
        'ckd_stage': stage,
        'stage_description': stage_description,
        'recommendations': recommendations
    }


def explain_prediction_with_shap(patient_data, model, scaler, feature_names, label_encoders, top_n=10):
    """
    Generate SHAP explanation for individual patient prediction
    
    Input:
    - patient_data: dict with patient data
    - model: trained model
    - scaler: fitted scaler
    - feature_names: list of feature names
    - label_encoders: dict of label encoders
    - top_n: number of top features to return
    
    Output:
    - Dictionary with SHAP analysis
    """
    
    # Create a copy and encode categorical features
    patient_data_encoded = patient_data.copy()
    
    # Encode categorical features
    categorical_features = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']
    for col in categorical_features:
        if col in label_encoders and col in patient_data_encoded:
            value = str(patient_data_encoded[col]).lower()
            try:
                patient_data_encoded[col] = label_encoders[col].transform([value])[0]
            except ValueError:
                patient_data_encoded[col] = 0
    
    # Prepare patient data
    clinical_features = [patient_data_encoded[f] for f in feature_names]
    features_scaled = scaler.transform([clinical_features])
    features_df = pd.DataFrame(features_scaled, columns=feature_names)
    
    # Initialize SHAP explainer
    print("   Initializing SHAP explainer...")
    if hasattr(model, 'feature_importances_'):  # Tree-based models
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(features_df)
        
        # Handle binary classification output
        # SHAP returns a list of arrays for multi-class, one array per class
        if isinstance(shap_values, list):
            # For binary classification, list has 2 arrays (one per class)
            # Each array has shape (n_samples, n_features)
            # Use class 0 (CKD)
            shap_values_positive = shap_values[0]
        else:
            # Single array
            shap_values_positive = shap_values
            
        if isinstance(explainer.expected_value, (list, np.ndarray)):
            base_value = explainer.expected_value[0] if len(explainer.expected_value) > 1 else explainer.expected_value
        else:
            base_value = explainer.expected_value
    else:
        # Use KernelExplainer for other models
        def model_predict(X):
            return model.predict_proba(X)[:, 0]  # CKD probability
        
        explainer = shap.KernelExplainer(model_predict, features_df)
        shap_values_positive = explainer.shap_values(features_df)
        base_value = explainer.expected_value
    
    # Convert to numpy array and get patient SHAP values
    shap_values_positive = np.array(shap_values_positive)
    
    # For a single patient, extract the SHAP values
    # Expected shape after selection: (n_features,)
    if shap_values_positive.ndim == 3:
        # Shape: (n_samples, n_features, n_classes)
        # Extract: first sample, all features, first class (CKD = class 0)
        patient_shap_values = shap_values_positive[0, :, 0]
    elif shap_values_positive.ndim == 2:
        # Shape: (n_samples, n_features) - take first sample
        patient_shap_values = shap_values_positive[0, :]
    elif shap_values_positive.ndim == 1:
        # Shape: (n_features,) - already correct
        patient_shap_values = shap_values_positive
    else:
        raise ValueError(f"Unexpected SHAP values shape: {shap_values_positive.shape}")
    
    # Ensure 1D
    patient_shap_values = np.array(patient_shap_values).flatten()
    
    # Validation
    if len(patient_shap_values) != len(feature_names):
        raise ValueError(f"SHAP values length ({len(patient_shap_values)}) does not match feature names length ({len(feature_names)})")
    
    # Create feature importance ranking with original values
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'shap_value': patient_shap_values,
        'abs_shap_value': np.abs(patient_shap_values),
        'feature_value': [patient_data.get(f, 'N/A') for f in feature_names],
        'impact_direction': ['↑ INCREASES' if float(x) > 0 else '↓ DECREASES' for x in patient_shap_values]
    }).sort_values('abs_shap_value', ascending=False)
    
    # Get top features
    top_features = feature_importance.head(top_n)
    
    return {
        'all_shap_values': patient_shap_values,
        'feature_importance': feature_importance,
        'top_features': top_features,
        'base_value': base_value,
        'explainer': explainer,
        'features_df': features_df
    }


def visualize_shap_explanation(shap_explanation, patient_results, save_path='patient_shap_report.png'):
    """
    Create professional 2-panel SHAP visualization
    
    Left Panel: SHAP values bar chart
    Right Panel: Summary information
    """
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))
    
    # Left Panel: SHAP values
    top_features = shap_explanation['top_features']
    colors = ['#FF6B6B' if x > 0 else '#4ECDC4' for x in top_features['shap_value']]
    
    bars = ax1.barh(range(len(top_features)), top_features['shap_value'], 
                    color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax1.set_yticks(range(len(top_features)))
    ax1.set_yticklabels(top_features['feature'], fontsize=12, fontweight='bold')
    ax1.set_xlabel('SHAP Value (Impact on Prediction)', fontsize=13, fontweight='bold')
    ax1.set_title('Top 10 Features Affecting CKD Prediction\n(Red = Increases Risk, Blue = Decreases Risk)', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.axvline(x=0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    ax1.invert_yaxis()
    
    # Add value labels
    for i, (idx, row) in enumerate(top_features.iterrows()):
        value = row['shap_value']
        ax1.text(value + (0.02 if value > 0 else -0.02), i, 
                f'{value:.3f}', va='center', 
                ha='left' if value > 0 else 'right',
                fontweight='bold', fontsize=10)
    
    # Right Panel: Summary
    ax2.axis('off')
    
    summary_text = f"""
╔═══════════════════════════════════════════════════════════╗
║           PREDICTION SUMMARY REPORT                       ║
╚═══════════════════════════════════════════════════════════╝

🎯 CKD STATUS: {patient_results['prediction']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 CKD Probability:      {patient_results['ckd_probability']:.2f}%
📊 No CKD Probability:   {patient_results['no_ckd_probability']:.2f}%
🎚️  Confidence Level:     {patient_results['confidence']}
⚠️  Risk Level:           {patient_results['risk_level']}

🔬 KIDNEY FUNCTION ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   eGFR:  {patient_results['egfr']} mL/min/1.73m²
   Stage: {patient_results['ckd_stage']}
   
   {patient_results['stage_description']}

💡 TOP 5 RISK FACTORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # Add top 5 features with explanations
    for i, (idx, row) in enumerate(top_features.head(5).iterrows(), 1):
        impact = "increases" if row['shap_value'] > 0 else "decreases"
        summary_text += f"\n{i}. {row['feature']} {impact} risk"
        summary_text += f"\n   Impact: {abs(row['shap_value']):.3f} | Value: {row['feature_value']}"
    
    summary_text += f"\n\n{'━'*59}"
    summary_text += f"\n⚠️  CLINICAL RECOMMENDATIONS (Top 3)"
    summary_text += f"\n{'━'*59}"
    for i, rec in enumerate(patient_results['recommendations'][:3], 1):
        summary_text += f"\n{i}. {rec}"
    
    ax2.text(0.05, 0.95, summary_text, transform=ax2.transAxes, 
            fontsize=10.5, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=1', facecolor='#FFF8DC', alpha=0.9, edgecolor='black', linewidth=2))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✅ SHAP visualization saved to: {save_path}")
    
    return fig


def print_detailed_explanation(patient_results, shap_explanation):
    """
    Print comprehensive text report
    """
    
    print("\n" + "="*80)
    print("                      CKD PREDICTION REPORT")
    print("="*80)
    
    print(f"\n📊 PREDICTION RESULT:")
    print(f"   Status:              {patient_results['prediction']}")
    print(f"   CKD Probability:     {patient_results['ckd_probability']:.2f}%")
    print(f"   No CKD Probability:  {patient_results['no_ckd_probability']:.2f}%")
    print(f"   Confidence:          {patient_results['confidence']}")
    print(f"   Risk Level:          {patient_results['risk_level']}")
    
    print(f"\n🔬 KIDNEY FUNCTION ASSESSMENT:")
    print(f"   eGFR:                {patient_results['egfr']} mL/min/1.73m²")
    print(f"   CKD Stage:           {patient_results['ckd_stage']}")
    print(f"   Description:         {patient_results['stage_description']}")
    
    print(f"\n💡 FEATURE IMPORTANCE (SHAP Analysis):")
    print(f"   Top 10 features affecting this prediction:\n")
    
    top_features = shap_explanation['top_features']
    print(f"   {'Rank':<6} {'Feature':<12} {'Direction':<20} {'Impact':<12} {'Value':<12}")
    print(f"   {'-'*6} {'-'*12} {'-'*20} {'-'*12} {'-'*12}")
    
    for i, (idx, row) in enumerate(top_features.iterrows(), 1):
        print(f"   {i:<6} {row['feature']:<12} {row['impact_direction']:<20} {abs(row['shap_value']):<12.4f} {str(row['feature_value']):<12}")
    
    print(f"\n🎯 CLINICAL RECOMMENDATIONS:")
    for i, rec in enumerate(patient_results['recommendations'], 1):
        print(f"   {i}. {rec}")
    
    print("\n" + "="*80)


def complete_prediction_pipeline(patient_data, model, scaler, feature_names, label_encoders):
    """
    End-to-end prediction workflow
    
    This is the main function users will call
    """
    
    print("\n" + "="*80)
    print("                    🏥 CKD PREDICTION SYSTEM")
    print("="*80)
    
    # Validate input
    print("\n📋 Step 1: Validating patient data...")
    required_features = feature_names + ['sex']
    missing = [f for f in required_features if f not in patient_data]
    if missing:
        print(f"❌ Missing features: {missing}")
        return None, None
    
    print("✅ All required features present")
    
    # Make prediction
    print("\n🔮 Step 2: Making CKD prediction...")
    results = predict_ckd_with_stage(patient_data, model, scaler, feature_names, label_encoders)
    print("✅ Prediction complete")
    
    # Generate SHAP explanation
    print("\n💡 Step 3: Generating SHAP explanation...")
    shap_explanation = explain_prediction_with_shap(patient_data, model, scaler, feature_names, label_encoders)
    print("✅ SHAP analysis complete")
    
    # Display results
    print_detailed_explanation(results, shap_explanation)
    
    # Create visualization
    print("\n📊 Step 4: Creating visualization...")
    fig = visualize_shap_explanation(shap_explanation, results)
    plt.close()  # Close the figure to save memory
    
    print("\n✅ Complete prediction pipeline finished!")
    
    return results, shap_explanation


if __name__ == "__main__":
    print("\n" + "="*80)
    print("  CKD PREDICTION SYSTEM - Main Module")
    print("  This module contains all core functions for CKD prediction")
    print("  Run 'example_usage.py' to see the complete pipeline in action")
    print("="*80)

