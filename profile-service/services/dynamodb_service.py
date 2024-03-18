import boto3

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
        self.table_name = 'Profiles'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f"Table '{self.table_name}' already exists. Loading it.")
        except Exception as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                table = self.dynamodb.create_table(
                    TableName = 'Profiles',
                    KeySchema = [{
                        'AttributeName': 'username',
                        'KeyType': 'HASH'
                    }],
                    AttributeDefinitions = [{
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    }],
                    ProvisionedThroughput = {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                table.meta.client.get_waiter('table_exists').wait(TableName='Profiles')
                print('Profiles table created.')
            else:
                raise
        self.profiles_table = self.dynamodb.Table('Profiles')