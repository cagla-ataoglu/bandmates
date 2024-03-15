import boto3

def create_users_table(dynamodb):
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[{'AttributeName': 'UserID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'UserID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='Users')
    print("Table created successfully.")

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
    create_users_table(dynamodb)
