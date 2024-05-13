# Auth Service
The auth microservice responsible for handling operations on authentication and authorization.

## Tech Used
Cognito is used to authanticate and authorize users. Cognito is in AWS free tier however not in the free version of Localstack, regardless we userd Localstack in development via using a trial token. Localstack is used to replace Cognito in development. Boto3 is used to communicate with the AWS services. CherryPy, python are used to create a router. The microservice is containerized via docker.
