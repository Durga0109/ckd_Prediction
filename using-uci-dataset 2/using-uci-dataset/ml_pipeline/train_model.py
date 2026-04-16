"""
Train CKD Prediction Model

This script:
1. Loads and preprocesses the dataset
2. Trains XGBoost and Random Forest models
3. Evaluates model performance
4. Saves trained models and preprocessors

Run this script first before making predictions!
"""

from ckd_prediction_system import (
    load_and_preprocess_data,
    train_best_model,
    evaluate_model
)
import joblib

def main():
    """
    Main training pipeline
    """
    
    print("\n" + "="*80)
    print("         🚀 CKD MODEL TRAINING PIPELINE")
    print("="*80)
    
    # Step 1: Load and preprocess data
    print("\n📂 Loading and preprocessing data...")
    (X_train, X_val, X_test, y_train, y_val, y_test, 
     scaler, label_encoders, target_encoder, feature_names, knn_imputer) = load_and_preprocess_data()
    
    # Step 2: Train model
    print("\n🤖 Training models...")
    best_model, model_name = train_best_model(X_train, y_train, X_val, y_val)
    
    # Step 3: Evaluate on test set
    print("\n📊 Evaluating model on test set...")
    test_metrics = evaluate_model(best_model, X_test, y_test, target_encoder)
    
    # Step 4: Save everything
    import os
    MODELS_DIR = 'trained_models'
    
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print(f"\n📁 Created directory: {MODELS_DIR}")
        
    print("\n💾 Saving models and preprocessors to 'trained_models/'...")
    
    joblib.dump(best_model, os.path.join(MODELS_DIR, 'ckd_best_model.pkl'))
    print("   ✅ Model saved: ckd_best_model.pkl")
    
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
    
    print("\n" + "="*80)
    print("✅ TRAINING COMPLETE!")
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
    
    print("\n" + "="*80)
    
    return best_model, scaler, feature_names, label_encoders, target_encoder


if __name__ == "__main__":
    main()

