import sqlite3
import pandas as pd
import os

# Database path
db_path = "ckd_clinical.db"

if not os.path.exists(db_path):
    print(f"❌ Database file not found at: {db_path}")
    exit()

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    print("\n=== 🏥 CLINICIANS (Registered Users) ===")
    clinicians = pd.read_sql_query("SELECT id, email, full_name, specialization, created_at FROM clinicians", conn)
    if clinicians.empty:
        print("No clinicians found.")
    else:
        print(clinicians.to_string(index=False))

    print("\n\n=== 👥 PATIENTS ===")
    patients = pd.read_sql_query("SELECT id, full_name, age, sex, clinician_id FROM patients", conn)
    if patients.empty:
        print("No patients found.")
    else:
        print(patients.to_string(index=False))

    print("\n")
    conn.close()

except Exception as e:
    print(f"Error reading database: {e}")
