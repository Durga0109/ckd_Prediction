"""
Train CKD Prediction Model using XGBoost

This script:
1. Loads and preprocesses the dataset
2. Trains XGBoost model (skipping Random Forest)
3. Evaluates model performance
4. Saves trained models and preprocessors

Run this script to specifically use XGBoost instead of Random Forest!
"""

from ckd_prediction_system import load_and_preprocess_data, evaluate_model
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV

def train_xgboost_model(X_train, y_train, X_val, y_val):
    """
    Train XGBoost model specifically (without comparing to Random Forest)
    
    Returns:
    - best_model: trained XGBoost model
    - model_name: 'XGBoost'
    """
    
    print("\n" + "="*80)
    print("🤖 XGBOOST MODEL TRAINING")
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
    xgb_val_pred = xgb_grid.best_estimator_.predict(X_val)
    xgb_val_proba = xgb_grid.best_estimator_.predict_proba(X_val)[:, 1]
    xgb_val_score = roc_auc_score(y_val, xgb_val_proba)
    
    print(f"   ✅ XGBoost - CV Score: {xgb_grid.best_score_:.4f}, Val Score: {xgb_val_score:.4f}")
    print(f"   Best params: {xgb_grid.best_params_}")
    
    best_model = xgb_grid.best_estimator_
    best_model_name = 'XGBoost'
    
    print(f"\n🏆 Selected Model: {best_model_name}")
    print(f"   Cross-validation ROC-AUC: {xgb_grid.best_score_:.4f}")
    print(f"   Validation ROC-AUC: {xgb_val_score:.4f}")
    
    print("\n" + "="*80)
    
    return best_model, best_model_name

def main():
    """
    Main training pipeline using XGBoost
    """
    
    print("\n" + "="*80)
    print("         🚀 CKD MODEL TRAINING PIPELINE (XGBOOST)")
    print("="*80)
    
    # Step 1: Load and preprocess data
    print("\n📂 Loading and preprocessing data...")
    (X_train, X_val, X_test, y_train, y_val, y_test, 
     scaler, label_encoders, target_encoder, feature_names, knn_imputer) = load_and_preprocess_data()
    
    # Step 2: Train XGBoost model
    print("\n🤖 Training XGBoost model...")
    best_model, model_name = train_xgboost_model(X_train, y_train, X_val, y_val)
    
    # Step 3: Evaluate on test set
    print("\n📊 Evaluating model on test set...")
    test_metrics = evaluate_model(best_model, X_test, y_test, target_encoder)
    
    # Step 4: Save everything
    print("\n💾 Saving models and preprocessors...")
    
    joblib.dump(best_model, 'ckd_xgboost_model.pkl')
    print("   ✅ XGBoost model saved: ckd_xgboost_model.pkl")
    
    # Also save as best_model for compatibility with existing code
    joblib.dump(best_model, 'ckd_best_model.pkl')
    print("   ✅ Model saved as best_model: ckd_best_model.pkl")
    
    joblib.dump(scaler, 'ckd_scaler.pkl')
    print("   ✅ Scaler saved: ckd_scaler.pkl")
    
    joblib.dump(feature_names, 'ckd_feature_names.pkl')
    print("   ✅ Feature names saved: ckd_feature_names.pkl")
    
    joblib.dump(label_encoders, 'ckd_label_encoders.pkl')
    print("   ✅ Label encoders saved: ckd_label_encoders.pkl")
    
    joblib.dump(target_encoder, 'ckd_target_encoder.pkl')
    print("   ✅ Target encoder saved: ckd_target_encoder.pkl")
    
    joblib.dump(knn_imputer, 'ckd_knn_imputer.pkl')
    print("   ✅ KNN imputer saved: ckd_knn_imputer.pkl")
    
    # Save metrics
    joblib.dump(test_metrics, 'ckd_test_metrics.pkl')
    print("   ✅ Test metrics saved: ckd_test_metrics.pkl")
    
    print("\n" + "="*80)
    print("✅ XGBOOST TRAINING COMPLETE!")
    print("="*80)
    
    print(f"\n📊 Final Test Performance:")
    print(f"   Model: {model_name}")
    print(f"   ROC-AUC: {test_metrics['roc_auc']:.4f}")
    print(f"   Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"   F1-Score: {test_metrics['f1']:.4f}")
    
    print("\n🎯 Next Steps:")
    print("   1. Run 'python example_usage.py' to test predictions")
    print("   2. Use the saved models for real-time predictions")
    print("   3. Check 'patient_shap_report.png' for visualization")
    print("   4. Run 'streamlit run app.py' to use the web interface")
    
    print("\n" + "="*80)
    
    return best_model, scaler, feature_names, label_encoders, target_encoder


if __name__ == "__main__":
    main()
