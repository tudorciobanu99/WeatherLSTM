import sys
sys.path.append("/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.extract.extract import run_extract
from src.transform.transform import run_transform
from src.load.load import run_load
from src.utils.common import today

default_args = {
    'owner': 'Tudor',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 23, 11, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

locations = ['London', 'Paris']
run_date = today()
end_date = run_date - timedelta(days=5)
start_date = end_date - timedelta(days=6)
db_name = 'src/database/weather.duckdb'

with DAG(
    'etl_dag',
    default_args = default_args,
    description = 'ETL pipeline for weather data.',
    schedule = '0 1 * * MON',
    catchup = True,
    tags = ['weather']
) as dag:

    extract_task = PythonOperator(
        task_id = 'extract',
        python_callable = run_extract,
        op_kwargs = {
            'locations': locations, 
            'start_date': start_date.strftime('%Y-%m-%d'), 
            'end_date': end_date.strftime('%Y-%m-%d')
        }
    )

    transform_task = PythonOperator(
        task_id = 'transform',
        python_callable = run_transform
    )

    load_task = PythonOperator(
        task_id = 'load',
        python_callable = run_load,
        op_kwargs = {'db_name': db_name}
    )

    extract_task >> transform_task >> load_task