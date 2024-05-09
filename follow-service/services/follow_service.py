import boto3
import json

class FollowService:
    def __init__(self):
        self.environment = os.getenv('ENV', 'development')
        if self.environment == 'production':
            self.dynamodb = boto3.resource('dynamodb')
        else:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')

        self.follow = 'Follow'
        self.follow_requests = 'Follow_requests'

        self.follow_table = ensure_follow_table(self.follow)
        self.follow_requests_table = ensure_follow_table(self.follow_requests)

    def ensure_follow_table(self, table_name):
        try:
            self.dynamodb.Table(table_name).load()
            print(f'Table {self.table_name} already exists. Loading it.')
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'follower',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'following',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'follower',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'following',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            print('Connections table created.')
        return self.dynamodb.Table(self.table_name)
        
    def send_follow_request(self, follower, following):
        self.follow_requests_table.put_item(
            Item={
                'follower': follower,
                'following': following
            }
        )

    def get_follow_requests(self, username):
        requests = []
        last_evaluated_key = None
        while True:
            response = self.follow_requests_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('follower').eq(username),
                ExclusiveStartKey=last_evaluated_key
            )
            requests.extend([item['following'] for item in response.get('Items', [])])
            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break
        return requests

    def create_follow(self, follower, following):
        self.follow_table.put_item(
            Item={
                'follower': follower,
                'following': following
            }
        )

    def get_followings(self, username):
        followings = []
        last_evaluated_key = None
        while True:
            response = self.follow_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('follower').eq(username),
                ExclusiveStartKey=last_evaluated_key
            )
            followings.extend([item['following'] for item in response.get('Items', [])])
            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break
        return followings
        
