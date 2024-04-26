variable "aws_region" {
  description = "AWS region to deploy the resources into"
  type        = string
  default     = "us-west-2"
}

variable "lambda_endpoint" {
  description = "Endpoint for Lambda services"
  type        = string
  default     = "http://localhost:4566" # Default to LocalStack endpoint; override for AWS
}

variable "cognito_endpoint" {
  description = "Endpoint for Cognito services"
  type        = string
  default     = "http://localhost:4566" # Default to LocalStack endpoint; override for AWS
}
