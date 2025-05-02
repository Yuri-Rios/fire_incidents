from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    dag_id='run_pyspark_script',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['spark', 'local']
) as dag:

    run_spark = BashOperator(
        task_id='run_spark_script',
        bash_command='python /workspaces/fire_incidents/main.py'
    )
