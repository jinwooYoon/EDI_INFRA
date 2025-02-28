from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# LocalExecutor가 정상 작동하는지 확인하는 테스트용 함수
def print_hello():
    print("✅ LocalExecutor 테스트 성공! Airflow가 정상 동작 중입니다.")

# DAG 기본 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
with DAG(
    'local_executor_test3',
    default_args=default_args,
    description='LocalExecutor 테스트 DAG',
    schedule_interval=timedelta(minutes=5),  # 5분마다 실행
    catchup=False
) as dag:

    task_hello = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello
    )

    task_hello  # 실행

