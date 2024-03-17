import boto3

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
        self.table_name = 'Users'
        # Ensure Users table exists
        try:
            self.dynamodb.Table(self.table_name).load()
            print(f"Table '{self.table_name}' already exists. Loading it.")
        except Exception as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                table = self.dynamodb.create_table(
                    TableName='Users',
                    KeySchema=[{'AttributeName': 'Username', 'KeyType': 'HASH'}],
                    AttributeDefinitions=[{'AttributeName': 'Username', 'AttributeType': 'S'}],
                    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                )
                table.meta.client.get_waiter('table_exists').wait(TableName='Users')
                print("Users table created.")
            else:
                raise
        self.users_table = self.dynamodb.Table('Users')

    def signup_user(self, username, email):
        self.users_table.put_item(
            Item={
                'Username': username,
                'Email': email
            }
        )
        print('dynamo done')

    def get_user(self, username):
        response = self.users_table.get_item(Key={'Username': username})
        
        if 'Item' in response:
            return response['Item']
        else:
            return None
