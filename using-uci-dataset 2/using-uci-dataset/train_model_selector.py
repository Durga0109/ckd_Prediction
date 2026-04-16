"""
CKD Prediction Model Selector

This script allows you to train and select between different models:
1. XGBoost
2. Random Forest
3. Both (compare and select the best)

Usage:
    python3 train_model_selector.py --model [xgboost/randomforest/both]
"""

import argparse
from ckd_prediction_system import load_and_preprocess_data, evaluate_model
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
import os

def train_xgboost_model(X_train, y_train, X_val, y_val):
    """Train XGBoost model"""
    
    print("\n" + "="*80)
    print("🤖 TRAINING XGBOOST MODEL")
    print("="*80)
    
    # XGBoost parameters
    print("\nTraining XGBoost...")
    xgb_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 4, 5, 6],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0]
    }
    
    # Initialize and train XGBoost model
    xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss', use_label_encoder=False)
    xgb_grid = GridSearchCV(xgb_model, xgb_params, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    xgb_grid.fit(X_train, y_train)
    
    # Evaluate on validation set
    xgb_val_proba = xgb_grid.best_estimator_.predict_proba(X_val)[:, 1]
    xgb_val_score = roc_auc_score(y_val, xgb_val_proba)
    
    print(f"   ✅ XGBoost - CV Score: {xgb_grid.best_score_:.4f}, Val Score: {xgb_val_score:.4f}")
    print(f"   Best params: {xgb_grid.best_params_}")
    
    return xgb_grid.best_estimator_, xgb_val_score

def train_random_forest_model(X_train, y_train, X_val, y_val):
    """Train Random Forest model"""
    
    print("\n" + "="*80)
    print("🤖 TRAINING RANDOM FOREST MODEL")
    print("="*80)
    
    # Random Forest parameters
    print("\nTraining Random Forest...")
    rf_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 15, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    # Initialize and train Random Forest model
    rf_model = RandomForestClassifier(random_state=42, n_jobs=-1)
    rf_grid = GridSearchCV(rf_model, rf_params, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    rf_grid.fit(X_train, y_train)
    
    # Evaluate on validation set
    rf_val_proba = rf_grid.best_estimator_.predict_proba(X_val)[:, 1]
    rf_val_score = roc_auc_score(y_val, rf_val_proba)
    
    print(f"   ✅ Random Forest - CV Score: {rf_grid.best_score_:.4f}, Val Score: {rf_val_score:.4f}")
    print(f"   Best params: {rf_grid.best_params_}")
    
    return rf_grid.best_estimator_, rf_val_score

def save_models(best_model, model_name, scaler, feature_names, label_encoders, target_encoder, knn_imputer, test_metrics):
    """Save all models and preprocessors"""
    MODELS_DIR = 'trained_models'
    
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print(f"\n📁 Created directory: {MODELS_DIR}")
        
    print(f"\n💾 Saving models and preprocessors to '{MODELS_DIR}/'...")
    
    # Save the selected model as the best model
    joblib.dump(best_model, os.path.join(MODELS_DIR, 'ckd_best_model.pkl'))
    print(f"   ✅ Selected model ({model_name}) saved as: ckd_best_model.pkl")
    
    # Also save with specific name
    model_filename = f"ckd_{model_name.lower().replace(' ', '_')}_model.pkl"
    joblib.dump(best_model, os.path.join(MODELS_DIR, model_filename))
    print(f"   ✅ Model also saved as: {model_filename}")
    
    # Save preprocessors
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'ckd_scaler.pkl'))
    print("   ✅ Scaler saved: ckd_scaler.pkl")
    
    joblib.dump(feature_names, os.path.join(MODELS_DIR, 'ckd_feature_names.pkl'))
    print("   ✅ Feature names saved: ckd_feature_names.pkl")
    
    joblib.dump(label_encoders, os.path.join(MODELS_DIR, 'ckd_label_encoders.pkl'))
    print("   ✅ Label encoders saved: ckd_label_encoders.pkl")
    
    joblib.dump(target_encoder, os.path.join(MODELS_DIR, 'ckd_target_encoder.pkl'))
    print("   ✅ Target encoder saved: ckd_target_encoder.pkl")
    
    joblib.dump(knn_imputer, os.path.join(MODELS_DIR, 'ckd_knn_imputer.pkl'))
    print("   ✅ KNN imputer saved: ckd_knn_imputer.pkl")
    
    # Save metrics
    joblib.dump(test_metrics, os.path.join(MODELS_DIR, 'ckd_test_metrics.pkl'))
    print("   ✅ Test metrics saved: ckd_test_metrics.pkl")
    
    # Save model selection info
    with open('model_selection.txt', 'w') as f:
        f.write(f"Selected Model: {model_name}\n")
        f.write(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Test ROC-AUC: {test_metrics['roc_auc']:.4f}\n")
        f.write(f"Test Accuracy: {test_metrics['accuracy']:.4f}\n")
        f.write(f"Test F1-Score: {test_metrics['f1']:.4f}\n")
    
    print("   ✅ Model selection info saved: model_selection.txt")

def main():
    """Main function to train and select models"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train and select CKD prediction models')
    parser.add_argument('--model', type=str, choices=['xgboost', 'randomforest', 'both'], 
                        default='both', help='Model to train (default: both)')
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print(f"         🚀 CKD MODEL TRAINING PIPELINE - {args.model.upper()}")
    print("="*80)
    
    # Step 1: Load and preprocess data
    print("\n📂 Loading and preprocessing data...")
    (X_train, X_val, X_test, y_train, y_val, y_test, 
     scaler, label_encoders, target_encoder, feature_names, knn_imputer) = load_and_preprocess_data()
    
    # Step 2: Train selected model(s)
    models = {}
    
    if args.model == 'xgboost' or args.model == 'both':
        xgb_model, xgb_val_score = train_xgboost_model(X_train, y_train, X_val, y_val)
        models['XGBoost'] = (xgb_model, xgb_val_score)
    
    if args.model == 'randomforest' or args.model == 'both':
        rf_model, rf_val_score = train_random_forest_model(X_train, y_train, X_val, y_val)
        models['Random Forest'] = (rf_model, rf_val_score)
    
    # Step 3: Select the best model or use the specified one
    if args.model == 'both':
        best_model_name = max(models.keys(), key=lambda k: models[k][1])
        best_model = models[best_model_name][0]
        print(f"\n🏆 Best Model Selected: {best_model_name}")
        print(f"   Validation ROC-AUC: {models[best_model_name][1]:.4f}")
    elif args.model == 'xgboost':
        best_model_name = 'XGBoost'
        best_model = models[best_model_name][0]
        print(f"\n🏆 Selected Model: {best_model_name}")
        print(f"   Validation ROC-AUC: {models[best_model_name][1]:.4f}")
    else:  # randomforest
        best_model_name = 'Random Forest'
        best_model = models[best_model_name][0]
        print(f"\n🏆 Selected Model: {best_model_name}")
        print(f"   Validation ROC-AUC: {models[best_model_name][1]:.4f}")
    
    # Step 4: Evaluate on test set
    print("\n📊 Evaluating model on test set...")
    test_metrics = evaluate_model(best_model, X_test, y_test, target_encoder)
    
    # Step 5: Save everything
    save_models(best_model, best_model_name, scaler, feature_names, 
                label_encoders, target_encoder, knn_imputer, test_metrics)
    
    print("\n" + "="*80)
    print("✅ TRAINING COMPLETE!")
    print("="*80)
    
    print(f"\n📊 Final Test Performance:")
    print(f"   Model: {best_model_name}")
    print(f"   ROC-AUC: {test_metrics['roc_auc']:.4f}")
    print(f"   Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"   F1-Score: {test_metrics['f1']:.4f}")
    
    print("\n🎯 Next Steps:")
    print("   1. Run 'python example_usage.py' to test predictions")
    print("   2. Run 'streamlit run app.py' to use the web interface")
    print("   3. Check 'patient_shap_report.png' for visualization")
    
    print("\n" + "="*80)
    
    return best_model, best_model_name


if __name__ == "__main__":
    main()
