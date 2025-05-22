from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

def run_spark_job():
    spark = SparkSession.builder \
        .appName("Flatten Patient JSON") \
        .master("local[*]") \
        .getOrCreate()

    df = spark.read.option("multiline", "true").json("/opt/airflow/dags/sample_patient.json")

    df_visits = df.select("patient_id", "name", explode("visits").alias("visit"))
    df_diagnoses = df_visits.select(
        "patient_id", "name",
        col("visit.visit_id"),
        col("visit.date").alias("visit_date"),
        explode("visit.diagnoses").alias("diagnosis"),
        col("visit.provider_notes.text").alias("provider_notes"),
        col("visit.provider_notes.author").alias("provider_author")
    )
    df_treatments = df_diagnoses.select(
        "patient_id", "name", "visit_id", "visit_date", "provider_notes", "provider_author",
        col("diagnosis.code").alias("diagnosis_code"),
        col("diagnosis.description").alias("diagnosis_description"),
        explode("diagnosis.treatments").alias("treatment")
    )
    df_flat = df_treatments.select(
        "patient_id", "name", "visit_id", "visit_date", "provider_notes", "provider_author",
        "diagnosis_code", "diagnosis_description",
        col("treatment.drug").alias("drug"), col("treatment.dose").alias("dose")
    )

    df_flat.show(truncate=False, vertical=True)
    spark.stop()

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

with DAG("spark_patient_dag",
         schedule_interval=None,
         catchup=False,
         default_args=default_args) as dag:

    spark_task = PythonOperator(
        task_id="run_spark_job",
        python_callable=run_spark_job
    )
