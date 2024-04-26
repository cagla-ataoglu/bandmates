resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_lambda_function" "example_lambda" {
  function_name = "MyExampleFunction"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_execution_role.arn

  # Assume the ZIP file is previously created and uploaded to an S3 bucket
  s3_bucket = "my-lambda-deployments"
  s3_key    = "lambda_function.zip"
}

# You might also want to setup an API Gateway here
