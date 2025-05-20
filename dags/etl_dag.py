from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}

def run_etl_script():
    subprocess.run(["python", "/opt/airflow/dags/transform_and_load.py"], check=True)

with DAG(
    dag_id="healthcare_etl_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["etl"],
) as dag:

    run_etl_task = PythonOperator(
        task_id="run_etl_task",
        python_callable=run_etl_script,
    )
