provider "aws" {
  region = var.aws_region

  # Use environment variables to switch between AWS and LocalStack
  access_key                  = "mock_access_key" # Not used in AWS but needed for LocalStack
  secret_key                  = "mock_secret_key" # Not used in AWS but needed for LocalStack
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_force_path_style         = true

  endpoints {
    lambda        = var.lambda_endpoint
    cognito-idp   = var.cognito_endpoint
  }
}
