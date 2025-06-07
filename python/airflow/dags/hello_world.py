from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def say_hello():
    print("👋 Hello Airflow!")

with DAG(
    dag_id='hello_world',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['example']
) as dag:
    task = PythonOperator(
        task_id='say_hello',
        python_callable=say_hello
    )
