import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()
bucket = "s3://s3-data-bootcamp-maufbl0808109231/"
path_log = "raw/log_reviews.csv"

log_review_df = spark.read.csv(
    bucket + path_log, sep=',', header=True, inferSchema=True, multiLine=True)

log_review_df = (spark
      .read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(bucket + path_log))

log_review_df = log_review_df.withColumn('log', regexp_replace(
    'log', '<reviewlog><log><logDate>', '')).withColumn('log', regexp_replace(
        'log', '</phoneNumber></log></reviewlog>', ''))

log_review_df = log_review_df.withColumn('log', regexp_replace(
    'log', '\<(.*?)\>', ';')).withColumn('log', regexp_replace(
        'log', ';;', ';'))

log_review_df = log_review_df.withColumn(
    'log_date', split(log_review_df['log'],
                      ';').getItem(0))
log_review_df = log_review_df.withColumn(
    'device', split(log_review_df['log'],
                    ';').getItem(1))
log_review_df = log_review_df.withColumn(
    'location', split(log_review_df['log'],
                      ';').getItem(2))
log_review_df = log_review_df.withColumn(
    'os', split(log_review_df['log'],
                ';').getItem(3))
log_review_df = log_review_df.withColumn(
    'ip_address', split(log_review_df['log'],
                        ';').getItem(4))
log_review_df = log_review_df.withColumn(
    'phoneNumber', split(log_review_df['log'],
                         ';').getItem(5))
