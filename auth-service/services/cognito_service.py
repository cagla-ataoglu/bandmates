import boto3
import os
import jwt
import requests
import time
import json

class CognitoService:
    def __init__(self):
        """
            Initializes CognitoService with the necessary resources and configurations.
        """
        self.environment = os.getenv('ENV', 'development')
        self.region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

        if self.environment == 'production':
            self.cognito = boto3.client('cognito-idp')
        elif self.environment == 'test':
            self.cognito = boto3.client('cognito-idp')
        else:
            self.cognito = boto3.client('cognito-idp', endpoint_url='http://localstack:4566')

        self.jwks_cache = None
        self.jwks_last_updated = 0
        self.jwks_cache_duration = 3600

        self.pool_name = os.getenv('USER_POOL_NAME')
        self.pool_id = ''
        pools = self.cognito.list_user_pools(MaxResults=10)
        for pool in pools.get('UserPools', []):
            if pool['Name'] == self.pool_name:
                print(f"User pool '{self.pool_name}' already exists. Loading it. ID: {pool['Id']}")
                self.pool_id = pool['Id']
        if self.pool_id == '':
            response = self.cognito.create_user_pool(PoolName=self.pool_name)
            self.pool_id = response['UserPool']['Id']
            print("User pool created.")

        self.client_name = os.getenv('CLIENT_NAME')
        self.client_id = ''
        clients = self.cognito.list_user_pool_clients(UserPoolId=self.pool_id, MaxResults=10)
        for client in clients.get('UserPoolClients', []):
            if client['ClientName'] == self.client_name:
                print(f"App client '{self.client_name}' already exists. Loading it. ID: {client['ClientId']}")
                self.client_id = client['ClientId']
        if self.client_id == '':
            response = self.cognito.create_user_pool_client(UserPoolId=self.pool_id, ClientName=self.client_name)
            self.client_id = response['UserPoolClient']['ClientId']
            print("Client created.")

        if self.environment == 'production':
            self.jwks_url_base =f"https://cognito-idp.{self.region}.amazonaws.com/{self.pool_id}"
        else:
            self.jwks_url_base = f"http://localstack:4566/{self.pool_id}"
        

    def signup_user(self, username, password, email):
        """
            Signs up a user in the Cognito user pool.

            Args:
                username (str): The username of the user.
                password (str): The password of the user.
                email (str): The email address of the user.

            Returns:
                dict: Response from Cognito.
        """
        response = self.cognito.sign_up(
            ClientId=self.client_id,
            Username=username,
            Password=password,
            UserAttributes=[{'Name': 'email', 'Value': email}]
        )
        self.cognito.admin_confirm_sign_up(
            UserPoolId=self.pool_id,
            Username=username
        )
        return response

    def change_password(self, access_token, old_password, new_password):
        """
            Changes the password of a user.

            Args:
                access_token (str): The access token of the user.
                old_password (str): The old password of the user.
                new_password (str): The new password to set.

            Returns:
                dict: Response indicating success or failure.
        """
        try:
            response = self.cognito.change_password(
                PreviousPassword=old_password,
                ProposedPassword=new_password,
                AccessToken=access_token
            )
            return {'status': 'success', 'message': 'Password changed successfully.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def authenticate_user(self, username, password):
        """
            Authenticates a user with username and password.

            Args:
                username (str): The username of the user.
                password (str): The password of the user.

            Returns:
                dict: Authentication tokens.
        """
        response = self.cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': username, 'PASSWORD': password},
            ClientId=self.client_id
        )
        return {
            'id_token': response['AuthenticationResult']['IdToken'],
            'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken'],
        }

    def get_jwks(self):
        """
            Retrieves the JWKS (JSON Web Key Set).

            Returns:
                dict: JWKS data.
        """
        current_time = time.time()
        if not self.jwks_cache or current_time - self.jwks_last_updated > self.jwks_cache_duration:
            jwks_url = self.jwks_url_base + "/.well-known/jwks.json"
            self.jwks_cache = requests.get(jwks_url).json()
            self.jwks_last_updated = current_time
        return self.jwks_cache

    def validate_token(self, token):
        """
            Validates a JWT token.

            Args:
                token (str): The JWT token to validate.

            Returns:
                dict: Validation result.
        """
        try:
            jwks = self.get_jwks()
            public_keys = {}
            for jwk in jwks['keys']:
                kid = jwk['kid']
                public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            kid = jwt.get_unverified_header(token)['kid']
            public_key = public_keys[kid]
            decoded_token = jwt.decode(token, key=public_key, algorithms=['RS256'])

            return {'status': 'success', 'user_info': decoded_token}
        except jwt.exceptions.InvalidTokenError as e:
            return {'status': 'error', 'message': str(e)}
