import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.ml.feature import Tokenizer, StopWordsRemover

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()
bucket = "s3://s3-data-bootcamp-maufbl0808109231/"
path_movie_review = "raw/movie_review.csv"
movie_review = (spark
      .read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(bucket + path_movie_review))

tokenizer = Tokenizer(inputCol="review_str", outputCol="words")
remover = StopWordsRemover(inputCol="words", outputCol="words_filtered")
movie_review = tokenizer.transform(movie_review)
movie_review = remover.transform(movie_review)
movie_review = movie_review.withColumn("positive_review", when(
    array_contains("words_filtered", 'good'), 1).otherwise(0))
movie_review = movie_review.withColumn('insert_date', current_timestamp())
movie_review = movie_review.drop('review_str',
             'words',
             'words_filtered')

movie_review.write.mode('overwrite').parquet(bucket + 'stage/movie_reviews')
