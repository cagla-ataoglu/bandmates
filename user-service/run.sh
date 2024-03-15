#!/bin/bash

python services/dynamodb_service.py
python services/cognito_service.py
python controller.py

echo "LocalStack is ready?"
