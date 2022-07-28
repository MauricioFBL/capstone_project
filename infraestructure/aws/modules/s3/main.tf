resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket

  versioning {
    enabled = var.versioning
  }

  tags = {
    Name = "s3-data-bootcamp"
  }
}

resource "aws_s3_bucket_object" "object_raw" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "raw/"
  source   = "/dev/null"
}
resource "aws_s3_bucket_object" "object_stage" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "stage/"
  source   = "/dev/null"
}
resource "aws_s3_bucket_object" "object_scripts" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "scripts/"
  source   = "/dev/null"
}
resource "aws_s3_bucket_object" "object_jars" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "jars/"
  source   = "/dev/null"
}
resource "aws_s3_bucket_object" "object_movie" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "raw/movie_reviews.csv"
  source   = "data/movie_review.csv"
  etag     = filemd5("data/movie_review.csv")
}
resource "aws_s3_bucket_object" "object_log" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "raw/log_reviews.csv"
  source   = "data/log_reviews.csv"
  etag     = filemd5("data/log_reviews.csv")
}
resource "aws_s3_bucket_object" "object_purchase" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "raw/user_purchase.csv"
  source   = "data/user_purchase.csv"
  etag     = filemd5("data/user_purchase.csv")
}
resource "aws_s3_bucket_object" "object_jar" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "jars/spark-xml_2.12-0.15.0.jar"
  source   = "jars/spark-xml_2.12-0.15.0.jar"
  etag     = filemd5("jars/spark-xml_2.12-0.15.0.jar")
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