import boto3
import os

class CognitoService:
    def __init__(self):
        self.cognito = boto3.client('cognito-idp', endpoint_url='http://localstack:4566')
        
        self.pool_name = os.getenv('USER_POOL_NAME')
        try:
            response = self.cognito.describe_user_pool(UserPoolId=self.pool_name)
            print("User pool exists.")
        except self.cognito.exceptions.ResourceNotFoundException:
            response = self.cognito.create_user_pool(PoolName=self.pool_name)
            print("User pool created.")
        self.pool_id = response['UserPool']['Id']

        self.client_name = os.getenv('CLIENT_NAME')
        self.client_id = ''
        try:
            response = self.cognito.list_user_pool_clients(UserPoolId=self.pool_id, MaxResults=60)
            for tmp in response['UserPoolClients']:
                if tmp['ClientName'] == self.client_name:
                    existing_client = tmp
                    break
            
            if existing_client:
                print("Client already exists.")
                self.client_id = existing_client['ClientId']
            else:
                raise Exception("App client not found.")
        except Exception as e:
            response = self.cognito.create_user_pool_client(UserPoolId=self.pool_id, ClientName=self.client_name)
            self.client_id = response['UserPoolClient']['ClientId']
            print("Client created.")

    def register_user(self, username, password, email):
        try:
            response = self.cognito.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=[{'Name': 'email', 'Value': email}]
            )
            return {'status': 'success', 'data': response}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    cognito_service = CognitoService()
