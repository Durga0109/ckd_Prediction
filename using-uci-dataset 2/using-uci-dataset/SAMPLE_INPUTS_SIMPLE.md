# Simplified Sample Inputs for CKD Prediction App

This document provides simplified versions of the sample inputs for quick copy-paste into the Streamlit app or command-line tools.

## CKD Patient Examples (Copy-Paste Format)

### Patient 1
```
Age: 48
Blood Pressure: 80
Specific Gravity: 1.020
Albumin: 1
Sugar: 0
Red Blood Cells: normal
Pus Cell: normal
Pus Cell Clumps: notpresent
Bacteria: notpresent
Blood Glucose Random: 121
Blood Urea: 36
Serum Creatinine: 1.2
Sodium: 135
Potassium: 4.2
Hemoglobin: 15.4
Packed Cell Volume: 44
White Blood Cell Count: 7800
Red Blood Cell Count: 5.2
Hypertension: yes
Diabetes Mellitus: yes
Coronary Artery Disease: no
Appetite: good
Pedal Edema: no
Anemia: no
```

### Patient 2 (High Creatinine)
```
Age: 53
Blood Pressure: 90
Specific Gravity: 1.020
Albumin: 2
Sugar: 0
Red Blood Cells: abnormal
Pus Cell: abnormal
Pus Cell Clumps: present
Bacteria: notpresent
Blood Glucose Random: 70
Blood Urea: 107
Serum Creatinine: 7.2
Sodium: 114
Potassium: 3.7
Hemoglobin: 9.5
Packed Cell Volume: 29
White Blood Cell Count: 12100
Red Blood Cell Count: 3.7
Hypertension: yes
Diabetes Mellitus: yes
Coronary Artery Disease: no
Appetite: poor
Pedal Edema: no
Anemia: yes
```

### Patient 3 (Elderly with CKD)
```
Age: 68
Blood Pressure: 70
Specific Gravity: 1.015
Albumin: 3
Sugar: 1
Red Blood Cells: normal
Pus Cell: normal
Pus Cell Clumps: present
Bacteria: notpresent
Blood Glucose Random: 208
Blood Urea: 72
Serum Creatinine: 2.1
Sodium: 138
Potassium: 5.8
Hemoglobin: 9.7
Packed Cell Volume: 28
White Blood Cell Count: 12200
Red Blood Cell Count: 3.4
Hypertension: yes
Diabetes Mellitus: yes
Coronary Artery Disease: yes
Appetite: poor
Pedal Edema: yes
Anemia: no
```

## Non-CKD Patient Examples (Copy-Paste Format)

### Patient 1 (Young Healthy)
```
Age: 23
Blood Pressure: 80
Specific Gravity: 1.025
Albumin: 0
Sugar: 0
Red Blood Cells: normal
Pus Cell: normal
Pus Cell Clumps: notpresent
Bacteria: notpresent
Blood Glucose Random: 70
Blood Urea: 36
Serum Creatinine: 1.0
Sodium: 150
Potassium: 4.6
Hemoglobin: 17.0
Packed Cell Volume: 52
White Blood Cell Count: 9800
Red Blood Cell Count: 5.0
Hypertension: no
Diabetes Mellitus: no
Coronary Artery Disease: no
Appetite: good
Pedal Edema: no
Anemia: no
```

### Patient 2 (Middle-aged Healthy)
```
Age: 45
Blood Pressure: 80
Specific Gravity: 1.025
Albumin: 0
Sugar: 0
Red Blood Cells: normal
Pus Cell: normal
Pus Cell Clumps: notpresent
Bacteria: notpresent
Blood Glucose Random: 82
Blood Urea: 49
Serum Creatinine: 0.6
Sodium: 147
Potassium: 4.4
Hemoglobin: 15.9
Packed Cell Volume: 46
White Blood Cell Count: 9100
Red Blood Cell Count: 4.7
Hypertension: no
Diabetes Mellitus: no
Coronary Artery Disease: no
Appetite: good
Pedal Edema: no
Anemia: no
```

### Patient 3 (Older Healthy)
```
Age: 60
Blood Pressure: 80
Specific Gravity: 1.025
Albumin: 0
Sugar: 0
Red Blood Cells: normal
Pus Cell: normal
Pus Cell Clumps: notpresent
Bacteria: notpresent
Blood Glucose Random: 131
Blood Urea: 10
Serum Creatinine: 0.5
Sodium: 146
Potassium: 5.0
Hemoglobin: 14.5
Packed Cell Volume: 41
White Blood Cell Count: 10700
Red Blood Cell Count: 5.1
Hypertension: no
Diabetes Mellitus: no
Coronary Artery Disease: no
Appetite: good
Pedal Edema: no
Anemia: no
```

## For Command-Line Tools

### For test_simple.py (CKD Patient)
```
python3 test_simple.py --age 53 --sc 7.2 --bp 90 --sg 1.020 --al 2 --su 0 --rbc abnormal --pc abnormal --pcc present --ba notpresent --bgr 70 --bu 107 --sod 114 --pot 3.7 --hemo 9.5 --pcv 29 --wbcc 12100 --rbcc 3.7 --htn yes --dm yes --cad no --appet poor --pe no --ane yes --save
```

### For test_simple.py (Non-CKD Patient)
```
python3 test_simple.py --age 45 --sc 0.6 --bp 80 --sg 1.025 --al 0 --su 0 --rbc normal --pc normal --pcc notpresent --ba notpresent --bgr 82 --bu 49 --sod 147 --pot 4.4 --hemo 15.9 --pcv 46 --wbcc 9100 --rbcc 4.7 --htn no --dm no --cad no --appet good --pe no --ane no --save
```

## Key Values to Test Different Scenarios

### To Test High-Probability CKD
- **Serum Creatinine**: >2.0
- **Blood Urea**: >100
- **Hemoglobin**: <10
- **Albumin**: 3-4
- **Hypertension**: yes
- **Diabetes**: yes

### To Test Borderline Cases
- **Serum Creatinine**: 1.3-1.5
- **Blood Urea**: 40-60
- **Hemoglobin**: 11-12
- **Albumin**: 1
- **Hypertension**: yes
- **Diabetes**: no

### To Test Clear Non-CKD
- **Serum Creatinine**: <1.0
- **Blood Urea**: <30
- **Hemoglobin**: >14
- **Albumin**: 0
- **Hypertension**: no
- **Diabetes**: no
