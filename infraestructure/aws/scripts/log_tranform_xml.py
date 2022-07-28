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

customSchema = StructType([
    StructField("logDate", StringType(), True),
    StructField("device", StringType(), True),
    StructField("location", StringType(), True),
    StructField("os", StringType(), True),
    StructField("ipAddress", StringType(), True),
    StructField("phoneNumber", StringType(), True)])

log = spark.read.format("xml").\
    option("rootTag", "reviewlog").\
    option("rowTag", "log").\
    load(bucket + path_log, schema=customSchema)
    
w = Window.orderBy(lit(1))
log = log.withColumn('id_review', row_number().over(w))
log.write.mode('overwrite').parquet(bucket + 'stage/log_reviews')
