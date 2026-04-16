# Switching Between ML Models for CKD Prediction

This guide explains how to easily switch between XGBoost and Random Forest models for your CKD Prediction System.

## Quick Start: Model Selector Script

I've created a unified script that lets you choose which model to use:

```bash
# To train and use XGBoost
python3 train_model_selector.py --model xgboost

# To train and use Random Forest
python3 train_model_selector.py --model randomforest

# To train both and use the best one
python3 train_model_selector.py --model both
```

## How Model Switching Works

The `train_model_selector.py` script:

1. Loads and preprocesses the dataset
2. Trains the model(s) you specified
3. Saves the selected model as `ckd_best_model.pkl`
4. Also saves model-specific files (e.g., `ckd_xgboost_model.pkl` or `ckd_random_forest_model.pkl`)
5. Creates a `model_selection.txt` file with information about the selected model

After running this script, all your existing code (app.py, example_usage.py, etc.) will automatically use the model you selected since it's saved as `ckd_best_model.pkl`.

## Comparing Models

To compare both models and select the best one:

```bash
python3 train_model_selector.py --model both
```

This will:
1. Train both XGBoost and Random Forest models
2. Compare their performance on the validation set
3. Select the better performing model
4. Save it as the default model

## Manual Model Switching

If you've already trained both models separately, you can manually switch between them:

```bash
# Switch to XGBoost
cp ckd_xgboost_model.pkl ckd_best_model.pkl

# Switch to Random Forest
cp ckd_random_forest_model.pkl ckd_best_model.pkl
```

## Model Characteristics

### XGBoost
- **Strengths**: Often better with complex relationships, handles missing values well
- **Performance**: Usually higher ROC-AUC and accuracy
- **Speed**: Faster inference time
- **Use when**: You need the highest possible accuracy

### Random Forest
- **Strengths**: Less prone to overfitting, more interpretable
- **Performance**: Good overall performance, robust to outliers
- **Speed**: Training can be faster with many features
- **Use when**: You need a more stable, interpretable model

## Checking Which Model is Currently Active

To check which model you're currently using:

```bash
# Option 1: Check the model_selection.txt file
cat model_selection.txt

# Option 2: Check the model type programmatically
python3 -c "
import joblib
model = joblib.load('ckd_best_model.pkl')
print(f'Current model: {type(model).__name__}')
"
```

## Tips for Model Selection

1. **XGBoost** is generally better for:
   - Highest possible accuracy
   - Complex, non-linear relationships
   - When you have sufficient data

2. **Random Forest** is generally better for:
   - More stable predictions
   - Better handling of outliers
   - When interpretability is important

3. **Try both** when:
   - You're not sure which will perform better
   - You want to validate your results with multiple models
   - You have time to train and compare

## Advanced: Ensemble of Models

For even better performance, you can create an ensemble of both models:

```python
import joblib
import numpy as np

# Load both models
xgb_model = joblib.load('ckd_xgboost_model.pkl')
rf_model = joblib.load('ckd_random_forest_model.pkl')

# Function to make ensemble predictions
def ensemble_predict(patient_data, scaler, feature_names, label_encoders):
    # Preprocess data (same as in complete_prediction_pipeline)
    # ...
    
    # Get predictions from both models
    xgb_pred = xgb_model.predict_proba(features_scaled)[0]
    rf_pred = rf_model.predict_proba(features_scaled)[0]
    
    # Average the probabilities (simple ensemble)
    ensemble_proba = (xgb_pred + rf_pred) / 2
    
    # Make final prediction
    ckd_status = "CKD" if ensemble_proba[0] > 0.5 else "No CKD"
    
    return ckd_status, ensemble_proba
```

## Troubleshooting

If you encounter any issues:

1. Make sure you have both models trained and saved:
   ```bash
   ls -l ckd_xgboost_model.pkl ckd_random_forest_model.pkl
   ```

2. Check that the model was saved correctly:
   ```bash
   ls -l ckd_best_model.pkl
   ```

3. If you see errors about incompatible models, retrain both models using the selector script:
   ```bash
   python3 train_model_selector.py --model both
   ```

## Next Steps

After selecting your preferred model:

1. Run the Streamlit app to see it in action:
   ```bash
   streamlit run app.py
   ```

2. Test predictions with example data:
   ```bash
   python3 example_usage.py
   ```

3. Make predictions with your own data:
   ```bash
   python3 predict.py
   ```

The beauty of this approach is that all your existing code will work with whichever model you choose, making it easy to switch and compare different models!
