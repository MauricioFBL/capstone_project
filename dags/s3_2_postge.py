from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.sql import BranchSQLOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

# General constants
DAG_ID = "aws_s3_2_postgre"
STABILITY_STATE = "stable"
CLOUD_PROVIDER = "aws"

# AWS constants
AWS_CONN_ID = "s3_conn"
S3_BUCKET_NAME = "s3-data-bootcamp-maufbl0808109231"
S3_KEY_NAME = "raw/user_purchase.csv"

# Postgres constants
POSTGRES_CONN_ID = "postgre_conn"
POSTGRES_SCHEMA_NAME = "dbname"
POSTGRES_TABLE_NAME = "user_purchase"

def ingest_data_from_s3(
    s3_bucket: str,
    s3_key: str,
    postgres_table: str,
    aws_conn_id: str = "aws_default",
    postgres_conn_id: str = "postgres_default",
):
    """Ingest data from an S3 location into a postgres table.
    Args:
        s3_bucket (str): Name of the s3 bucket.
        s3_key (str): Name of the s3 key.
        postgres_table (str): Name of the postgres table.
        aws_conn_id (str): Name of the aws connection ID.
        postgres_conn_id (str): Name of the postgres connection ID.
    """
    s3_hook = S3Hook(aws_conn_id=aws_conn_id)
    psql_hook = PostgresHook(postgres_conn_id)
    local_filename = s3_hook.download_file(key=s3_key, bucket_name=s3_bucket)
    psql_hook.copy_expert(sql = """COPY user_purchase(
                invoice_number,
                stock_code,
                detail,
                quantity,
                invoice_date,
                unit_price,
                customer_id,
                country) 
                FROM STDIN
                DELIMITER ',' CSV HEADER;""", filename = local_filename)

    

def ingest_data_from_s3_new(
    s3_bucket: str,
    s3_key: str,
    postgres_table: str,
    aws_conn_id: str = "aws_default",
    postgres_conn_id: str = "postgres_default",):
    #Open Postgres Connection
    s3_hook = S3Hook(aws_conn_id=aws_conn_id)
    local_filename = s3_hook.download_file(key=s3_key, bucket_name=s3_bucket)
    get_postgres_conn = PostgresHook(postgres_conn_id).get_conn()
    cur = get_postgres_conn.cursor()
    with open(local_filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO user_purchase VALUES (%s, %s, %s, %s,%s, %s, %s, %s)", row)
        get_postgres_conn.commit()


with DAG(
    dag_id=DAG_ID,
    schedule_interval="@once",
    start_date=days_ago(1),
    tags=[CLOUD_PROVIDER, STABILITY_STATE],
) as dag:
    start_workflow = DummyOperator(task_id="start_workflow")

    verify_key_existence = S3KeySensor(
        task_id="verify_key_existence",
        aws_conn_id=AWS_CONN_ID,
        bucket_name=S3_BUCKET_NAME,
        bucket_key=S3_KEY_NAME,
    )

    create_table_entity = PostgresOperator(
        task_id="create_table_entity",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"""
            CREATE TABLE IF NOT EXISTS {POSTGRES_TABLE_NAME} (
                invoice_number varchar(10),
                stock_code varchar(20),
                detail varchar(1000),
                quantity int,
                invoice_date timestamp,
                unit_price numeric(8,3),
                customer_id int,
                country varchar(20)
            )
        """,
    )

    clear_table = PostgresOperator(
        task_id="clear_table",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"DELETE FROM {POSTGRES_TABLE_NAME}",
    )
    continue_process = DummyOperator(task_id="continue_process")

    ingest_data = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data_from_s3,
        op_kwargs={
            "aws_conn_id": AWS_CONN_ID,
            "postgres_conn_id": POSTGRES_CONN_ID,
            "s3_bucket": S3_BUCKET_NAME,
            "s3_key": S3_KEY_NAME,
            "postgres_table": POSTGRES_TABLE_NAME,
        },
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    validate_data = BranchSQLOperator(
        task_id="validate_data",
        conn_id=POSTGRES_CONN_ID,
        sql=f"SELECT COUNT(*) AS total_rows FROM {POSTGRES_TABLE_NAME}",
        follow_task_ids_if_false=[continue_process.task_id],
        follow_task_ids_if_true=[clear_table.task_id],
    )

    end_workflow = DummyOperator(task_id="end_workflow")

    (
        start_workflow
        >> verify_key_existence
        >> create_table_entity
        >> validate_data
    )
    validate_data >> [clear_table, continue_process] >> ingest_data
    ingest_data >> end_workflow

    dag.doc_md = __doc__