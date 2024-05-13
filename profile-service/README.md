# Profile Service
The profile microservice responsible for handling operations on profiles.

## Tech Used
DynamoDB is used to create tables to store information on profiles. An S3 Bucket is used for the profile pictures. In development Localstack is used to create local replicas of DynamoDB tables and the S3 bucket. Boto3 is used to communicate with the AWS services. CherryPy, python are used to create a router. The microservice is containerized via docker.

### Unit tests
Unit tests cover functions in the service.
