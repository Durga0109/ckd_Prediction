# Probability-Stage Relationship in CKD Prediction

This document explains how the CKD probability affects the displayed CKD stage in the prediction system.

## The Issue

The original system had a discrepancy: patients with very high CKD probabilities (e.g., 99%) were sometimes displayed with lower CKD stages (e.g., Stage 3) based solely on their eGFR value. This created confusion since a very high probability of CKD should typically correlate with a more severe stage.

## The Solution

We've implemented a probability-based stage adjustment system that ensures high-probability CKD predictions are reflected with appropriately severe stages:

### Probability-Based Stage Adjustments

| CKD Probability | Stage Adjustment |
|-----------------|------------------|
| ≥ 95%           | Stage 5 (regardless of eGFR) |
| ≥ 90%           | At least Stage 4 |
| ≥ 85%           | At least Stage 3 |
| < 85%           | Based on eGFR only |

### How It Works

1. **First, calculate the eGFR-based stage** using the standard CKD-EPI equation and KDIGO guidelines
2. **Then, apply probability-based adjustments** if the probability exceeds certain thresholds
3. **Finally, display the adjusted stage** with a note explaining the adjustment

## Code Implementation

The adjustment happens in two key places:

### 1. In the Stage Display Logic

```python
# Determine the correct stage based on prediction, probability and eGFR
if prediction == "No CKD":
    # If prediction is No CKD, show Stage 0
    display_stage = 0
    stage_description = "No CKD - Normal kidney function"
else:
    # For CKD prediction, adjust stage based on probability if needed
    if ckd_probability >= 95:
        # For very high probability CKD (≥95%), set to stage 5
        display_stage = 5
        stage_description = "Stage 5 (G5): Kidney failure (end-stage)"
    elif ckd_probability >= 90 and stage < 4:
        # For high probability CKD (≥90%), ensure stage is at least 4
        display_stage = 4
        stage_description = "Stage 4 (G4): Severely decreased kidney function"
    elif ckd_probability >= 85 and stage < 3:
        # For moderately high probability CKD (≥85%), ensure stage is at least 3
        display_stage = 3
        stage_description = "Stage 3a (G3a): Mild to moderately decreased kidney function"
    else:
        # Use the stage based on eGFR
        display_stage = stage
        stage_description = results['stage_description']
```

### 2. In the Gauge Chart Visualization

```python
# Determine the display stage based on probability and eGFR
if ckd_probability >= 95:
    # For very high probability CKD (≥95%), highlight stage 5
    display_stage = 5
elif ckd_probability >= 90 and stage < 4:
    # For high probability CKD (≥90%), highlight at least stage 4
    display_stage = 4
elif ckd_probability >= 85 and stage < 3:
    # For moderately high probability CKD (≥85%), highlight at least stage 3
    display_stage = 3
else:
    display_stage = stage
```

### 3. In the Recommendations

The recommendations are also adjusted based on probability:

```python
# For very high probability cases, adjust recommendations regardless of eGFR
if prediction_binary == 0 and ckd_probability >= 95:  # CKD with very high probability
    recommendations.extend([
        "🚨 URGENT: Immediate nephrology consultation required",
        # More urgent recommendations...
    ])
elif prediction_binary == 0 and ckd_probability >= 90:  # CKD with high probability
    recommendations.extend([
        "⚠️ Urgent nephrology referral (within 1-2 weeks)",
        # More serious recommendations...
    ])
```

## Explanation Note

For transparency, we've added an explanatory note when the stage is adjusted:

```python
# For high stages, show probability-based adjustment note if applicable
probability_note = ""
if ckd_probability >= 95 and results['ckd_stage'] < 5:
    probability_note = f"<p><em>Note: Stage adjusted to 5 due to very high CKD probability ({ckd_probability:.1f}%)</em></p>"
elif ckd_probability >= 90 and results['ckd_stage'] < 4:
    probability_note = f"<p><em>Note: Stage adjusted to 4 due to high CKD probability ({ckd_probability:.1f}%)</em></p>"
elif ckd_probability >= 85 and results['ckd_stage'] < 3:
    probability_note = f"<p><em>Note: Stage adjusted to 3 due to elevated CKD probability ({ckd_probability:.1f}%)</em></p>"
```

## Medical Rationale

This adjustment is medically justified because:

1. **High CKD probability indicates significant kidney damage** that may not yet be reflected in the eGFR
2. **Multiple biomarkers contribute to the probability** beyond just creatinine (which is used for eGFR)
3. **Early intervention is critical** for high-probability cases, even if eGFR is not severely reduced
4. **Risk stratification should consider all factors**, not just eGFR

## Example Cases

### Case 1: 99% CKD Probability with eGFR 42 mL/min/1.73m²
- **Original System**: Stage 3b (based only on eGFR)
- **New System**: Stage 5 (adjusted due to very high 99% probability)
- **Explanation**: The extremely high probability indicates severe kidney disease despite moderate eGFR reduction

### Case 2: 92% CKD Probability with eGFR 55 mL/min/1.73m²
- **Original System**: Stage 2 (based only on eGFR)
- **New System**: Stage 4 (adjusted due to high 92% probability)
- **Explanation**: The high probability suggests significant kidney damage not fully reflected in eGFR

### Case 3: 75% CKD Probability with eGFR 40 mL/min/1.73m²
- **Original System**: Stage 3b (based on eGFR)
- **New System**: Stage 3b (no adjustment needed, probability <85%)
- **Explanation**: The moderate probability doesn't warrant stage adjustment

## Conclusion

This probability-based stage adjustment ensures that the displayed CKD stage accurately reflects both the eGFR-based kidney function AND the overall likelihood of kidney disease based on all clinical parameters. This provides a more comprehensive risk assessment for clinical decision-making.
