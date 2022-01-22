from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from spotify_etl import run_spotify_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 18),
    'email': ['airflow@example.com'],
    'email_on_failure': ['meriemismahlarbi@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description="My first ETL process",
    schedule_interval=timedelta(days=1),
)

def func():
    print("emploi fictif cace-dedi a Jacques Chirac.")

run_etl = PythonOperator(
    task_id = 'whole_spotify_etl',
    # python_callable=func,
    python_callable=run_spotify_etl,
    dag = dag,
)

run_etl
