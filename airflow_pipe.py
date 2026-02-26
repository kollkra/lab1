# airflow_pipe.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from train_model import preprocess_and_train

# Путь к файлу — положи рядом с DAG или укажи абсолютный путь
DATA_PATH = "/path/to/your/synthetic_cars_2025.csv"   # ← измени на реальный путь!
PROCESSED_PATH = "synthetic_cars_clean.csv"

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='synthetic_cars_price_prediction',
    default_args=default_args,
    description='Train model on synthetic cars dataset',
    start_date=datetime(2025, 3, 1),
    schedule='@daily',          # или '@hourly', '30 2 * * *' и т.д.
    catchup=False,
    max_active_runs=1,
    tags=['ml', 'cars', 'synthetic'],
) as dag:

    task_train = PythonOperator(
        task_id='preprocess_and_train_model',
        python_callable=preprocess_and_train,
        op_kwargs={
            'input_path': DATA_PATH,
            'processed_path': PROCESSED_PATH,
        },
    )
