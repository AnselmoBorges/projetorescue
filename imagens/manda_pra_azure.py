from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.wasb_hook import WasbHook
from airflow.models import Variable

pasta_dados = Variable.get("dados")
wb = WasbHook(wasb_conn_id='dados_rescue')
container_name = 'dados'
blob_name = 'arquivo_migrado.txt'
file_path = pasta_dados + '/teste.txt'

def check_connection():
    return (wb.check_for_blob(container_name, blob_name))

def file_upload():
    wb.load_file(file_path, container_name, blob_name)
    return('Blob uploaded sucessfully')

def respond():
    return 'Task ended'


default_args = {'owner': 'airflow',
                'start_date': datetime(2023,1,28),
                'concurrency': 1,
                'retries': 0
                }

with DAG('airflow_file_uploader',
         catchup=False,
         default_args=default_args,
         schedule_interval='*/10 * * * *',
         ) as dag:
        check_connection_opr = PythonOperator(task_id='connection',python_callable=check_connection)
        file_upload_opr = PythonOperator(task_id='file_uploader',python_callable=file_upload)
        opr_respond = PythonOperator(task_id='task_end',python_callable=respond)

check_connection_opr >> file_upload_opr >> opr_respond