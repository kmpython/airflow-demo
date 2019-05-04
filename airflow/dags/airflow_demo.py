import time
from builtins import range
from pprint import pprint
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.s3_key_sensor import S3KeySensor
from datetime import datetime
import airflow
import boto3
import random
import time
import sys

sys.path.append('/home/ubuntu')

from repo import read_csv, combiner, clean_data, download_file

s3_bucket = Variable.get("s3_bucket")               # airflow-bucket
s3_file = Variable.get("s3_file")                   # airflow-dl-file-num 
s3_file_trigger = Variable.get("s3-file-trigger")   # airflow-dl-file-*

def push_colname():
    return 'Dept'

def push_db_environment():
    options = ['branch_prod', 'branch_test', 'branch_dev']
    return random.choice(options)

args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 4, 8)
}

dag = DAG(
    dag_id='airflow_demo',
    default_args=args,
    schedule_interval=None
)

file_sensor = S3KeySensor(
    task_id='check_s3_for_file',
    bucket_key=s3_file_trigger,
    wildcard_match=True,
    provide_context=False,
    bucket_name=s3_bucket,
    timeout=18*60*60,
    poke_interval=30,
    dag=dag
)


job_dl_file = PythonOperator(
    task_id='download_file',
    provide_context=False,
    python_callable=download_file.run,
    op_kwargs={'bucket': s3_bucket, 'file':s3_file},
    dag=dag
)

job_1_move_files = PythonOperator(
    task_id='move_the_files',
    provide_context=False,
    python_callable=read_csv.run,
    dag=dag
)

job_2_combine_files = PythonOperator(
    task_id='combine_the_files',
    provide_context=False,
    python_callable=combiner.run, 
    dag=dag
)

job_push_col_name = PythonOperator (
    task_id='push_col_name',
    provide_context=False,
    python_callable=push_colname,
    dag=dag
)

job_3_clean_combine=PythonOperator(
    task_id='clean_combine_files',
    provide_context=True,
    python_callable=clean_data.run,
    dag=dag
)

dummy_generate_report=DummyOperator (
    task_id='generate_report',
    dag=dag
)

branch_db_env = BranchPythonOperator(
    task_id='branch_db_env',
    provide_context=False,
    python_callable=push_db_environment,
    dag=dag
)

file_sensor >> job_dl_file >> job_1_move_files
job_1_move_files >> job_2_combine_files
[job_push_col_name, job_2_combine_files] >> job_3_clean_combine
job_3_clean_combine >> dummy_generate_report
job_3_clean_combine >> branch_db_env

job_close = DummyOperator(
    task_id='END',
    trigger_rule='one_success',
    dag=dag
)

job_insert_db_prod = DummyOperator(
    task_id='branch_prod',
    dag=dag
)

job_insert_db_test = DummyOperator(
    task_id='branch_test',
    dag=dag
)

job_insert_db_dev = DummyOperator(
    task_id='branch_dev',
    dag=dag
)

branch_db_env >> job_insert_db_prod >> job_close
branch_db_env >> job_insert_db_test >> job_close
branch_db_env >> job_insert_db_dev >> job_close
