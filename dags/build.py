from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    dag_id='build_fire_incidents_database',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['spark', 'local']
) as dag:

    run_spark = BashOperator(
        task_id='build',
        bash_command='python /workspaces/fire_incidents/etl/database/ingestion.py'
    )
