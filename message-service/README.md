# Message Service
The message microservice responsible for handling operations on messages/chats.

## Tech Used
DynamoDB is used to create tables to store information on messages, create new chatrooms, send/receive messages. A websocket communication is used to achieve real-time chatting, and usual http communication is used for other endpoints. In development Localstack is used to create a local replica of the production tables. Boto3 is used to communicate with the AWS services. CherryPy, python are used to create a router. The microservice is containerized via docker.
