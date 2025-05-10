from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    dag_id='fire_incidents',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['spark', 'local']
) as dag:

    run_spark = BashOperator(
        task_id='ingestion',
        bash_command='python /workspaces/fire_incidents/etl/ingestion/warehouse_build.py'
    )
