# Using XGBoost for CKD Prediction

This guide explains how to use XGBoost instead of Random Forest for your CKD Prediction System.

## Quick Start

To use XGBoost, simply run:

```bash
python3 train_xgboost.py
```

This will:
1. Load and preprocess the dataset
2. Train an XGBoost model (skipping Random Forest)
3. Save the model as both `ckd_xgboost_model.pkl` and `ckd_best_model.pkl`

After running this script, all your existing code (app.py, example_usage.py, etc.) will automatically use the XGBoost model.

## Why Use XGBoost?

XGBoost (eXtreme Gradient Boosting) offers several advantages:

- **Performance**: Often achieves better performance than Random Forest
- **Speed**: Faster training and inference times
- **Regularization**: Built-in regularization to prevent overfitting
- **Feature Importance**: Provides detailed feature importance metrics
- **Missing Value Handling**: Can handle missing values natively

## Comparing XGBoost vs Random Forest

Both models are ensemble methods, but they work differently:

- **Random Forest**: Builds many independent decision trees and averages their predictions
- **XGBoost**: Builds trees sequentially, with each tree correcting the errors of previous trees

For medical applications like CKD prediction, XGBoost often performs better because:
- It can capture more complex relationships in the data
- It focuses on the most difficult-to-classify samples
- It has better regularization to avoid overfitting

## Using the XGBoost Model

After running `train_xgboost.py`, you can use the model with all existing code:

```bash
# Run the Streamlit app with XGBoost
streamlit run app.py

# Run examples with XGBoost
python3 example_usage.py

# Make predictions with XGBoost
python3 predict.py
```

## Checking XGBoost Feature Importance

XGBoost provides its own feature importance metrics, which you can visualize:

```python
import joblib
import matplotlib.pyplot as plt

# Load the XGBoost model
model = joblib.load('ckd_xgboost_model.pkl')
feature_names = joblib.load('ckd_feature_names.pkl')

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(range(len(model.feature_importances_)), model.feature_importances_, align='center')
plt.yticks(range(len(model.feature_importances_)), feature_names)
plt.xlabel('Feature Importance')
plt.title('XGBoost Feature Importance')
plt.tight_layout()
plt.savefig('xgboost_feature_importance.png')
plt.show()
```

## XGBoost Parameters

The script uses GridSearchCV to find the best parameters, but you can also manually set them:

```python
import xgboost as xgb

# Create XGBoost model with custom parameters
model = xgb.XGBClassifier(
    n_estimators=200,      # Number of trees
    max_depth=4,           # Maximum tree depth
    learning_rate=0.1,     # Learning rate
    subsample=0.8,         # Subsample ratio
    colsample_bytree=0.8,  # Column subsample ratio
    random_state=42
)
```

## Troubleshooting

If you encounter any issues:

1. Make sure you have the latest version of XGBoost installed:
   ```bash
   pip install --upgrade xgboost
   ```

2. Check that the model was saved correctly:
   ```bash
   ls -l ckd_xgboost_model.pkl ckd_best_model.pkl
   ```

3. If you see errors about missing features, make sure you're using the same preprocessing:
   ```python
   # Always use the same scaler and encoders
   scaler = joblib.load('ckd_scaler.pkl')
   label_encoders = joblib.load('ckd_label_encoders.pkl')
   ```

## Next Steps

After training your XGBoost model, you can:

1. Compare its performance with Random Forest
2. Try different hyperparameters to improve performance
3. Use the model in the Streamlit app
4. Export the model for deployment in other applications
