# Post Service
The post microservice responsible for handling operations on posts.

## Tech Used
DynamoDB is used to create tables to store information on posts and an S3 bucket is used to store the media contents. In development Localstack is used to replace a local replica of the production tables. Boto3 is used to communicate with the AWS services. CherryPy, python are used to create a router. The microservice is containerized via docker.

### Unit tests
Unit tests cover functions in the service.
