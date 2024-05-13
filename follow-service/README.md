# Follow Service
The follow microservice responsible for handling operations on follow relations.

## Tech Used
DynamoDB is used to create tables to store information on followers. In development Localstack is used to create a local replica of the production tables. Boto3 is used to communicate with the AWS services. CherryPy, python are used to create a router. The microservice is containerized via docker.

### Unit tests
Unit tests cover functions in the service.
