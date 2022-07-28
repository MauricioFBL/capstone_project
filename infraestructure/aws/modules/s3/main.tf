resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket

  versioning {
    enabled = var.versioning
  }

  tags = {
    Name = "s3-data-bootcamp"
  }
}

resource "aws_s3_bucket_object" "object_movie" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "movie_reviews.csv"
  source   = "raw/movie_review.csv"
  etag     = filemd5("raw/movie_review.csv")
}
resource "aws_s3_bucket_object" "object_log" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "log_reviews.csv"
  source   = "raw/log_reviews.csv"
  etag     = filemd5("raw/log_reviews.csv")
}
resource "aws_s3_bucket_object" "object_purchase" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "user_purchase.csv"
  source   = "raw/user_purchase.csv"
  etag     = filemd5("raw/user_purchase.csv")
}
resource "aws_s3_bucket_object" "object_jar" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "jars/spark-xml_2.12-0.15.0.jar"
  source   = "jars/spark-xml_2.12-0.15.0.jar"
  etag     = filemd5("jars/spark-xml_2.12-0.15.0.jar")
}
resource "aws_s3_bucket_object" "object_stage" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "stage/"
  source   = "/dev/null"
}
resource "aws_s3_bucket_object" "object_logs_script" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "scripts/log_transformation.py"
  source   = "scripts/log_transformation.py"
  etag     = filemd5("scripts/log_transformation.py")
}
resource "aws_s3_bucket_object" "object_moviess_script" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "scripts/movie_transformation.py"
  source   = "scripts/movie_transformation.py"
  etag     = filemd5("scripts/movie_transformation.py")
}