# hello_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def say_hello():
    print("Hello Airflow!")

with DAG(
    dag_id='hello_airflow',
    start_date=datetime(2025, 6, 1),
    #schedule_interval='*/3 * * * *',  # 3분마다 실행
    schedule_interval='*/1 * * * *',  # 3분마다 실행
    catchup=False
) as dag:
    task = PythonOperator(
        task_id='say_hello_task',
        python_callable=say_hello
    )
