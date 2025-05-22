import json
import os
import pandas as pd
from sqlalchemy import create_engine

# Create database engine
db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/medica")
engine = create_engine(db_url)

def upsert_df(df, table_name, key_column):
    """Insert or update a DataFrame into a database table using PostgreSQL upsert logic."""
    with engine.begin() as conn:
        for _, row in df.iterrows():
            keys = list(row.keys())
            values = [row[k] for k in keys]

            insert_cols = ", ".join(keys)
            insert_vals = ", ".join(["%s"] * len(values))
            update_stmt = ", ".join([f"{col}=EXCLUDED.{col}" for col in keys if col != key_column])

            sql = f"""
                INSERT INTO {table_name} ({insert_cols})
                VALUES ({insert_vals})
                ON CONFLICT ({key_column}) DO UPDATE SET {update_stmt};
            """

            conn.execute(sql, values)

def validate(df, name):
    """Validate a DataFrame for nulls and date formatting."""
    print(f"Validating {name}")
    if df.isnull().values.any():
        print(f"{name} contains null values!")

    if "date" in df.columns:
        print(f"{name} contains date field!")
        try:
            pd.to_datetime(df["date"])
            print("Date format check passed")
        except Exception as e:
            print(f"{name} has invalid date format: {e}")

# Get the absolute path of the current Python file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Join it with your filename
file_path = os.path.join(base_dir, "sample_patient.json")

# Load JSON data
with open(file_path) as f:
    data = json.load(f)

# Extract data into separate tables
patients, visits, diagnoses, treatments = [], [], [], []

for patient in data:
    patients.append({
        "patient_id": patient["patient_id"],
        "name": patient["name"]
    })

    for visit in patient["visits"]:
        visits.append({
            "visit_id": visit["visit_id"],
            "patient_id": patient["patient_id"],
            "date": visit["date"],
            "provider_notes_text": visit["provider_notes"]["text"],
            "provider_notes_author": visit["provider_notes"]["author"]
        })

        for diag in visit["diagnoses"]:
            diag_id = f"{visit['visit_id']}_{diag['code']}"
            diagnoses.append({
                "diagnosis_id": diag_id,
                "visit_id": visit["visit_id"],
                "code": diag["code"],
                "description": diag["description"]
            })

            for treat in diag["treatments"]:
                treatments.append({
                    "treatment_id": f"{diag_id}_{treat['drug']}",
                    "diagnosis_id": diag_id,
                    "drug": treat["drug"],
                    "dose": treat["dose"]
                })

# Convert lists to DataFrames
df_patients = pd.DataFrame(patients)
df_visits = pd.DataFrame(visits)
df_diagnoses = pd.DataFrame(diagnoses)
df_treatments = pd.DataFrame(treatments)

# Validate data
validate(df_patients, 'patients')
validate(df_visits, 'visits')

# Upsert data into database
upsert_df(df_patients, "patients", "patient_id")
upsert_df(df_visits, "visits", "visit_id")
upsert_df(df_diagnoses, "diagnoses", "diagnosis_id")
upsert_df(df_treatments, "treatments", "treatment_id")
