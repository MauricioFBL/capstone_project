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
  source   = "data/movie_review.csv"
  etag     = filemd5("data/movie_review.csv")
}
resource "aws_s3_bucket_object" "object_log" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "log_reviews.csv"
  source   = "data/log_reviews.csv"
  etag     = filemd5("data/log_reviews.csv")
}
resource "aws_s3_bucket_object" "object_purchase" {
  bucket   = aws_s3_bucket.bucket.id
  key      = "user_purchase.csv"
  source   = "data/user_purchase.csv"
  etag     = filemd5("data/user_purchase.csv")
}