from airflow.models import DAG
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from airflow.utils.dates import days_ago

DAG_ID = "glue_trigger"
STABILITY_STATE = "stable"
CLOUD_PROVIDER = "aws"
### glue job specific variables
glue_job_name_logs = "log_tranform"
glue_job_name_revs = "movie_transform"
glue_iam_role = "glue_admin"
region_name = "us-east-2"


with DAG(dag_id = DAG_ID, schedule_interval = "@once",
    start_date=days_ago(1),
    tags=[CLOUD_PROVIDER, STABILITY_STATE]) as dag:
    glue_job_step_logs = AwsGlueJobOperator(
        task_id = "glue_job_step_logs",
        script_location = "s3://s3-data-bootcamp-maufbl0808109231/scripts/log_transformation.py",
        job_name = glue_job_name_logs,
        job_desc = f"triggering glue job {glue_job_name_logs}",
        region_name = region_name,
        iam_role_name = glue_iam_role,
        num_of_dpus = 1,
        dag = dag
        )
    glue_job_step_revs = AwsGlueJobOperator(
        task_id = "glue_job_step_revs",
        script_location = "s3://s3-data-bootcamp-maufbl0808109231/scripts/movie_transformation.py",
        job_name = glue_job_name_revs,
        job_desc = f"triggering glue job {glue_job_name_logs}",
        region_name = region_name,
        iam_role_name = glue_iam_role,
        num_of_dpus = 1,
        dag = dag
        )
    glue_job_step_logs >> glue_job_step_revs
    dag.doc_md = __doc__