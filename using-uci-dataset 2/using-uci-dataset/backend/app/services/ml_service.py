"""
ML Service - Integration of CKD prediction model with SHAP and LIME explainers
Optimized to match the exact logic of the original working system.
"""
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional, List
import shap
from lime import lime_tabular
import os
from datetime import datetime

from ..config import get_settings

settings = get_settings()


class MLService:
    """Machine Learning service for CKD prediction with interpretability"""
    
    def __init__(self):
        """Initialize ML service and load models"""
        self.models_path = settings.ml_models_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.label_encoders = None
        self.shap_explainer = None
        self.lime_explainer = None
        self._load_models()
    
    def _load_models(self):
        """Load trained ML models and preprocessors"""
        try:
            # Load exact files from the training phase
            self.model = joblib.load(os.path.join(self.models_path, 'ckd_best_model.pkl'))
            self.scaler = joblib.load(os.path.join(self.models_path, 'ckd_scaler.pkl'))
            self.feature_names = joblib.load(os.path.join(self.models_path, 'ckd_feature_names.pkl'))
            self.label_encoders = joblib.load(os.path.join(self.models_path, 'ckd_label_encoders.pkl'))
            
            print("✅ ML models loaded successfully")
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise
    
    def _prepare_patient_data(self, patient_data: Dict) -> pd.DataFrame:
        """
        Prepare patient data for prediction.
        Matches the logic in predict_ckd_with_stage of the original system.
        """
        # Create a copy to avoid side effects
        data = patient_data.copy()
        
        # Categorical features list according to original system
        categorical_features = ['rbc', 'pc', 'pcc', 'ba', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane']
        
        # Encode categorical features matching original logic (lowercase + transform)
        for col in categorical_features:
            if col in self.label_encoders and col in data:
                # Original logic: convert to string, lowercase, strip
                value = str(data[col]).lower().strip()
                try:
                    data[col] = self.label_encoders[col].transform([value])[0]
                except (ValueError, KeyError, AttributeError):
                    # If value not in training set, default to 0 (usually the most common class)
                    data[col] = 0
            elif col in categorical_features:
                data[col] = 0 # Fallback
                
        # Extract only clinical features in the exact order the model expects
        try:
            ordered_features = [data.get(f, 0) for f in self.feature_names]
        except Exception as e:
            # If any feature is missing, we try to be safe
            ordered_features = []
            for f in self.feature_names:
                ordered_features.append(data.get(f, 0))
                
        # Scale features using the original scaler
        features_scaled = self.scaler.transform([ordered_features])
        
        # Return as DataFrame for SHAP/Model consistency
        return pd.DataFrame(features_scaled, columns=self.feature_names)
    
    def calculate_egfr(self, age: float, sex: str, creatinine: float) -> float:
        """Calculate eGFR using CKD-EPI 2021 equation (race-free)"""
        if str(sex).lower() == 'female':
            kappa = 0.7
            alpha = -0.241
            female_factor = 1.012
        else:
            kappa = 0.9
            alpha = -0.302
            female_factor = 1.0
        
        # Original math logic
        min_term = min(creatinine / kappa, 1.0) ** alpha
        max_term = max(creatinine / kappa, 1.0) ** (-1.200)
        age_term = 0.9938 ** age
        
        egfr = 142 * min_term * max_term * age_term * female_factor
        return round(egfr, 1)
    
    def determine_ckd_stage(self, egfr: float) -> Tuple[int, str]:
        """Determine CKD stage based on eGFR (KDIGO 2024 guidelines)"""
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
    
    def get_shap_explanation(self, features_df: pd.DataFrame, top_n: int = 10) -> Dict:
        """
        Generate SHAP explanation matching the original system logic.
        """
        try:
            # Initialize SHAP explainer if not already done
            if self.shap_explainer is None:
                # TreeExplainer is preferred for RandomForest/XGBoost
                self.shap_explainer = shap.TreeExplainer(self.model)
            
            # Calculate SHAP values
            shap_values = self.shap_explainer.shap_values(features_df)
            
            # EXTRACTING CORRECT CLASS (Original logic: Class 0 = CKD)
            # Binary classification in TreeExplainer can return list of arrays or single array
            if isinstance(shap_values, list):
                # Class 0 (CKD) is usually the first in the list
                shap_values_positive = shap_values[0]
            else:
                shap_values_positive = shap_values

            # Ensure we have a 1D array for the single instance
            if shap_values_positive.ndim == 2:
                # Shape (1, n_features) -> (n_features,)
                patient_shap_values = shap_values_positive[0]
            elif shap_values_positive.ndim == 3:
                # Shape (1, n_features, n_classes) -> take class 0
                patient_shap_values = shap_values_positive[0, :, 0]
            else:
                patient_shap_values = shap_values_positive.flatten()

            # Create feature importance ranking
            feature_importance = []
            for i, (feature, shap_val) in enumerate(zip(self.feature_names, patient_shap_values)):
                feature_importance.append({
                    'feature': feature,
                    'shap_value': float(shap_val),
                    'impact': 'increases' if shap_val > 0 else 'decreases'
                })
            
            # Sort by absolute impact
            feature_importance.sort(key=lambda x: abs(x['shap_value']), reverse=True)
            
            return {
                'top_features': feature_importance[:top_n],
                'all_shap_values': {f: float(v) for f, v in zip(self.feature_names, patient_shap_values)}
            }
        except Exception as e:
            print(f"Error in SHAP explanation: {e}")
            return {'top_features': [], 'all_shap_values': {}}
    
    def get_lime_explanation(self, features_df: pd.DataFrame, top_n: int = 10) -> Dict:
        """Generate LIME explanation for prediction"""
        try:
            if self.lime_explainer is None:
                # Generate a synthetic background dataset for meaningful perturbations.
                # LIME requires a representative training distribution to understand feature variance.
                # We simulate 200 patients in the scaled feature space (mean=0, std=1 per RobustScaler).
                np.random.seed(42)
                n_features = len(self.feature_names)
                background_data = np.random.normal(0, 1, size=(200, n_features))
                
                self.lime_explainer = lime_tabular.LimeTabularExplainer(
                    background_data,
                    feature_names=self.feature_names,
                    class_names=['CKD', 'No CKD'],
                    mode='classification',
                    discretize_continuous=False,  # Use continuous perturbation for clinical accuracy
                    sample_around_instance=True
                )
            
            exp = self.lime_explainer.explain_instance(
                features_df.values[0],
                self.model.predict_proba,
                num_features=top_n
            )
            
            lime_values = exp.as_list()
            feature_importance = []
            for feature_desc, weight in lime_values:
                # Strip logical operators from description for UI
                clean_name = feature_desc.split('<=')[0].split('>')[0].split('==')[0].strip()
                feature_importance.append({
                    'feature': clean_name,
                    'lime_weight': float(weight),
                    'impact': 'increases' if weight > 0 else 'decreases'
                })
            
            return {
                'top_features': feature_importance,
                'lime_score': float(exp.score)
            }
        except Exception as e:
            print(f"Error in LIME explanation: {e}")
            return {'top_features': [], 'lime_score': 0.0}
    
    def _generate_feature_recommendations(self, patient_data: Dict, top_features: List[Dict]) -> List[str]:
        """Generate targeted recommendations based on specific clinical parameters"""
        recs = []
        
        # 1. Blood Pressure
        bp = float(patient_data.get('bp', 0))
        if bp > 140:
            recs.append("💓 **Hypertension Management**: Target BP < 130/80 mmHg to slow CKD progression. Discuss ACEi/ARB therapy with patient.")
        
        # 2. Hemoglobin (Anemia)
        hemo = float(patient_data.get('hemo', 0))
        sex = str(patient_data.get('sex', 'male')).lower()
        low_hemo = 12.0 if sex == 'female' else 13.0
        if hemo < low_hemo:
            recs.append(f"🩸 **Anemia Detected** (Hemo: {hemo}): Evaluate for iron deficiency, B12/Folate levels, or erythropoietin-stimulating agents.")

        # 3. Serum Creatinine / eGFR
        sc = float(patient_data.get('sc', 0))
        if sc > 1.5:
             recs.append("⚠️ **Kidney Damage Risk**: High Serum Creatinine. Avoid nephrotoxic drugs like NSAIDs (Ibuprofen, Naproxen) and IV contrast.")

        # 4. Albumin (Proteinuria)
        al = int(patient_data.get('al', 0))
        if al >= 1:
            recs.append("🛡️ **Proteinuria Detected**: Significant albumin in urine indicates kidney damage. Strict BP control is essential.")

        # 5. Blood Glucose (Diabetes)
        bgr = float(patient_data.get('bgr', 0))
        if bgr > 180:
            recs.append("🍭 **Poor Glycemic Control**: Fasting blood sugar is high. Tighten diabetes management (Goal HbA1c < 7%) to prevent further nephropathy.")

        # 6. Potassium
        pot = float(patient_data.get('pot', 0))
        if pot > 5.5:
            recs.append("🍌 **Hyperkalemia Alert**: Potassium is dangerously high (> 5.5). Low-potassium diet and review of meds (like spironolactone) is URGENT.")
        elif pot < 3.5:
            recs.append("📉 **Hypokalemia**: Potassium levels are low. Consider dietary supplementation.")

        # 7. Sodium
        sod = float(patient_data.get('sod', 0))
        if sod < 135:
            recs.append("💧 **Hyponatremia**: Low sodium levels detected. Evaluate fluid intake and possible fluid restriction.")

        # 8. WBC (Infection)
        wbcc = float(patient_data.get('wbcc', 0))
        if wbcc > 11000:
            recs.append("🦠 **Possible Infection**: Elevated White Blood Cell Count. Screen for Urinary Tract Infection (UTI).")

        # Fallback if no specific issues found
        if not recs:
            recs.append("✅ Maintain current healthy lifestyle, hydration, and regular exercise.")
            
        return recs

    def predict(self, patient_data: Dict) -> Dict:
        """
        Main prediction method. Strictly aligned with original system.
        """
        # 1. Prepare Data
        features_df = self._prepare_patient_data(patient_data)
        
        # ========== DEBUG: Print raw and scaled input ==========
        # print("\n" + "="*70)
        # print("🔬 DIAGNOSTIC VERIFICATION LOG")
        # print("="*70)
        # print(f"\n📋 RAW INPUT DATA:")
        # for key in ['age', 'sex', 'sc', 'hemo', 'bp', 'bgr', 'bu', 'al', 'sg', 'htn', 'dm', 'ane']:
        #     print(f"   {key}: {patient_data.get(key, 'N/A')}")
        
        # print(f"\n📊 FEATURE ORDER (as model expects): {self.feature_names}")
        # print(f"📊 SCALED FEATURES (first row):")
        # for fname, fval in zip(self.feature_names, features_df.values[0]):
        #     print(f"   {fname}: {fval:.4f}")
        # ========== END DEBUG ==========
        
        # 2. Model Prediction
        # Original logic: 0 = CKD, 1 = Not CKD
        prediction_binary = self.model.predict(features_df)[0]
        prediction_prob = self.model.predict_proba(features_df)[0]
        
        ckd_prediction = "CKD" if prediction_binary == 0 else "No CKD"
        ckd_probability = float(prediction_prob[0]) # Prob of Class 0 (CKD)
        no_ckd_probability = float(prediction_prob[1]) # Prob of Class 1 (Not CKD)
        
        # ========== DEBUG: Print prediction results ==========
        # print(f"\n🎯 MODEL OUTPUT:")
        # print(f"   Binary Prediction: {prediction_binary} ({'CKD' if prediction_binary == 0 else 'No CKD'})")
        # print(f"   P(CKD)     = {ckd_probability:.4f} ({ckd_probability*100:.1f}%)")
        # print(f"   P(No CKD)  = {no_ckd_probability:.4f} ({no_ckd_probability*100:.1f}%)")
        # ========== END DEBUG ==========
        
        # 3. Confidence and Risk Level (Matching ckd_prediction_system logic)
        confidence_score = abs(ckd_probability - 0.5) * 2
        if confidence_score >= 0.4:
            confidence_level = "High"
        elif confidence_score >= 0.2:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"
            
        if ckd_probability >= 0.7:
            risk_level = "High"
        elif ckd_probability >= 0.5:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # 4. Calculate eGFR and stage
        egfr = None
        ckd_stage = None
        stage_description = None
        
        # We need specific fields for eGFR
        if patient_data.get('age') and patient_data.get('sex') and patient_data.get('sc'):
            egfr = self.calculate_egfr(
                float(patient_data['age']),
                str(patient_data['sex']),
                float(patient_data['sc'])
            )
            
            if ckd_prediction == "CKD":
                ckd_stage, stage_description = self.determine_ckd_stage(egfr)
            else:
                ckd_stage = 0
                stage_description = "No CKD - Normal kidney function"
        
        # # ========== DEBUG: Print eGFR and staging ==========
        # print(f"\n🫘 eGFR CALCULATION:")
        # print(f"   Age={patient_data.get('age')}, Sex={patient_data.get('sex')}, SC={patient_data.get('sc')}")
        # print(f"   eGFR = {egfr} mL/min")
        # print(f"   Stage = {ckd_stage} | {stage_description}")
        # ========== END DEBUG ==========
        
        # 5. Explanations
        shap_explanation = self.get_shap_explanation(features_df)
        lime_explanation = self.get_lime_explanation(features_df)
        
        # # ========== DEBUG: Print SHAP top features ==========
        # print(f"\n📈 TOP 5 SHAP FEATURES (sorted by |impact|):")
        # for feat in shap_explanation.get('top_features', [])[:5]:
        #     direction = "⬆️ RISK" if feat['shap_value'] > 0 else "⬇️ PROTECTIVE"
        #     print(f"   {feat['feature']:>10s}: {feat['shap_value']:+.4f} ({direction})")

        # print(f"\n🧪 TOP LIME FEATURES (sorted by |weight|):")
        # lime_feats = lime_explanation.get('top_features', [])
        # lime_sorted = sorted(lime_feats, key=lambda x: abs(x['lime_weight']), reverse=True)
        # for feat in lime_sorted:
        #     direction = "⬆️ SUPPORTS CKD" if feat['lime_weight'] > 0 else "⬇️ OPPOSES CKD"
        #     print(f"   {feat['feature']:>10s}: {feat['lime_weight']:+.6f} ({direction})")
        # print(f"\n   LIME R² Score: {lime_explanation.get('lime_score', 'N/A')}")
        # print("="*70 + "\n")
        # ========== END DEBUG ==========
        
        # 6. ENHANCED: Personalized Recommendations
        top_features = shap_explanation.get('top_features', [])
        detailed_recommendations = self._generate_feature_recommendations(patient_data, top_features)

        # 7. Generate clinical reasoning narrative from XAI outputs
        xai_narrative = self._generate_xai_narrative(
            patient_data, ckd_prediction, ckd_probability,
            top_features, lime_explanation, egfr, ckd_stage
        )

        return {
            'ckd_prediction': ckd_prediction,
            'ckd_probability': ckd_probability,
            'no_ckd_probability': no_ckd_probability,
            'confidence_level': confidence_level,
            'risk_level': risk_level,
            'egfr': egfr,
            'ckd_stage': ckd_stage,
            'stage_description': stage_description,
            'shap_values': shap_explanation,
            'lime_values': lime_explanation,
            'top_features': top_features,
            'recommendations': detailed_recommendations,
            'xai_narrative': xai_narrative
        }

    def _generate_xai_narrative(self, patient_data: Dict, prediction: str, probability: float,
                                 shap_features: List[Dict], lime_result: Dict,
                                 egfr: float, ckd_stage: int) -> Dict:
        """
        Generate a structured clinical reasoning narrative by interpreting 
        SHAP/LIME feature importance against the patient's actual biomarker values.
        """
        # Clinical reference ranges for contextual interpretation
        REFERENCE_RANGES = {
            'sc':   {'name': 'Serum Creatinine',      'unit': 'mg/dL',  'normal_low': 0.7, 'normal_high': 1.3, 'direction': 'high_is_bad'},
            'hemo': {'name': 'Hemoglobin',             'unit': 'g/dL',   'normal_low': 12.0, 'normal_high': 17.0, 'direction': 'low_is_bad'},
            'pcv':  {'name': 'Packed Cell Volume',     'unit': '%',       'normal_low': 36,   'normal_high': 50,   'direction': 'low_is_bad'},
            'bp':   {'name': 'Blood Pressure',         'unit': 'mmHg',   'normal_low': 60,   'normal_high': 120,  'direction': 'high_is_bad'},
            'bgr':  {'name': 'Blood Glucose (Random)', 'unit': 'mg/dL',  'normal_low': 70,   'normal_high': 140,  'direction': 'high_is_bad'},
            'bu':   {'name': 'Blood Urea',             'unit': 'mg/dL',  'normal_low': 7,    'normal_high': 20,   'direction': 'high_is_bad'},
            'al':   {'name': 'Urinary Albumin',        'unit': 'scale',  'normal_low': 0,    'normal_high': 0,    'direction': 'high_is_bad'},
            'sg':   {'name': 'Specific Gravity',       'unit': '',       'normal_low': 1.015,'normal_high': 1.025,'direction': 'low_is_bad'},
            'sod':  {'name': 'Sodium',                 'unit': 'mEq/L',  'normal_low': 135,  'normal_high': 145,  'direction': 'low_is_bad'},
            'pot':  {'name': 'Potassium',              'unit': 'mEq/L',  'normal_low': 3.5,  'normal_high': 5.0,  'direction': 'high_is_bad'},
            'wbcc': {'name': 'White Blood Cell Count',  'unit': '/µL',   'normal_low': 4500, 'normal_high': 11000,'direction': 'high_is_bad'},
            'rbcc': {'name': 'Red Blood Cell Count',    'unit': 'M/µL',  'normal_low': 4.2,  'normal_high': 6.1,  'direction': 'low_is_bad'},
            'htn':  {'name': 'Hypertension',           'unit': '',       'normal_low': 0,    'normal_high': 0,    'direction': 'categorical'},
            'dm':   {'name': 'Diabetes Mellitus',      'unit': '',       'normal_low': 0,    'normal_high': 0,    'direction': 'categorical'},
            'ane':  {'name': 'Anemia',                 'unit': '',       'normal_low': 0,    'normal_high': 0,    'direction': 'categorical'},
        }

        narrative = {}

        # --- 1. Overall Summary ---
        if prediction == "CKD":
            narrative['summary'] = (
                f"The algorithmic assessment indicates Chronic Kidney Disease with "
                f"{probability*100:.1f}% statistical confidence. "
                f"The estimated GFR is {egfr} mL/min, corresponding to Stage {ckd_stage}. "
                f"The following analysis explains the key biomarkers that contributed to this assessment."
            )
        else:
            narrative['summary'] = (
                f"The algorithmic assessment indicates no evidence of Chronic Kidney Disease, "
                f"with {(1-probability)*100:.1f}% confidence. "
                f"The estimated GFR is {egfr} mL/min, indicating normal kidney function. "
                f"Key protective factors are outlined below."
            )

        # --- 2. Top Risk Drivers with Clinical Context ---
        risk_drivers = []
        for feat in shap_features[:5]:  # Top 5 most impactful
            feature_key = feat['feature']
            shap_val = feat['shap_value']
            ref = REFERENCE_RANGES.get(feature_key)
            if not ref:
                continue

            raw_value = patient_data.get(feature_key, 'N/A')
            
            # Build contextual reasoning
            if ref['direction'] == 'categorical':
                value_str = str(raw_value).capitalize()
                if str(raw_value).lower() in ['yes', '1', 1]:
                    context = f"{ref['name']} is present, which is a known CKD comorbidity."
                else:
                    context = f"{ref['name']} is absent, which is a protective factor."
            else:
                try:
                    val = float(raw_value)
                    unit = ref['unit']
                    value_str = f"{val} {unit}"
                    
                    if ref['direction'] == 'high_is_bad' and val > ref['normal_high']:
                        deviation = val / ref['normal_high'] if ref['normal_high'] > 0 else 0
                        context = (f"Value is {deviation:.1f}x the upper reference limit "
                                   f"(normal: {ref['normal_low']}–{ref['normal_high']} {unit}). "
                                   f"Elevated levels indicate impaired renal function.")
                    elif ref['direction'] == 'low_is_bad' and val < ref['normal_low']:
                        context = (f"Value is below the normal range "
                                   f"(normal: {ref['normal_low']}–{ref['normal_high']} {unit}). "
                                   f"Reduced levels may indicate chronic disease progression.")
                    else:
                        context = f"Value is within the normal reference range ({ref['normal_low']}–{ref['normal_high']} {unit})."
                except (ValueError, TypeError):
                    value_str = str(raw_value)
                    context = "Unable to evaluate against reference range."

            risk_drivers.append({
                'biomarker': ref['name'],
                'key': feature_key,
                'value': value_str,
                'shap_impact': shap_val,
                'direction': 'Risk Factor' if shap_val > 0 else 'Protective Factor',
                'clinical_context': context
            })
        
        narrative['risk_drivers'] = risk_drivers

        # --- 3. SHAP-LIME Agreement Analysis ---
        lime_feats = lime_result.get('top_features', [])
        lime_score = lime_result.get('lime_score', 0.0)
        
        shap_top3 = set(f['feature'] for f in shap_features[:3])
        lime_top3 = set()
        if lime_feats:
            lime_sorted = sorted(lime_feats, key=lambda x: abs(x.get('lime_weight', 0)), reverse=True)
            lime_top3 = set(f['feature'] for f in lime_sorted[:3])
        
        overlap = shap_top3 & lime_top3
        agreement_pct = len(overlap) / 3 * 100 if shap_top3 else 0
        
        if agreement_pct >= 66:
            agreement_text = (f"Strong agreement ({agreement_pct:.0f}%): Both SHAP and LIME identify "
                              f"the same primary risk factors ({', '.join(overlap)}), "
                              f"indicating high confidence in the model's reasoning.")
        elif agreement_pct >= 33:
            agreement_text = (f"Partial agreement ({agreement_pct:.0f}%): SHAP and LIME partially overlap "
                              f"on key features ({', '.join(overlap) if overlap else 'limited overlap'}). "
                              f"The model's decision boundary may be non-linear in this region.")
        else:
            agreement_text = (f"Low agreement ({agreement_pct:.0f}%): SHAP and LIME identify different "
                              f"primary factors. SHAP (global) is recommended as the primary reference. "
                              f"LIME R² = {lime_score:.2f} suggests limited local fidelity.")

        narrative['agreement'] = {
            'text': agreement_text,
            'overlap_pct': agreement_pct,
            'lime_r2': lime_score
        }

        return narrative


# Global ML service instance
ml_service = MLService()
