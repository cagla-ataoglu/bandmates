import boto3
import json
import os

class FollowService:
    def __init__(self):
        self.environment = os.getenv('ENV', 'development')
        if self.environment == 'production':
            self.dynamodb = boto3.resource('dynamodb')
        else:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')

        self.follow = 'Follow'
        self.follow_requests = 'Follow_requests'

        self.follow_table = self.ensure_follow_table(self.follow)
        self.follow_requests_table = self.ensure_follow_table(self.follow_requests)

    def ensure_follow_table(self, table_name):
        try:
            self.dynamodb.Table(table_name).load()
            print(f'Table {table_name} already exists. Loading it.')
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            table = self.dynamodb.create_table(
                TableName=table_name,
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
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            print('Connections table created.')
        return self.dynamodb.Table(table_name)
        
    def send_follow_request(self, follower, following):
        try:
            self.follow_requests_table.put_item(
                Item={
                    'follower': follower,
                    'following': following
                },
                ConditionExpression="attribute_not_exists(follower) AND attribute_not_exists(following)"
            )
            print("Follow request sent successfully.")
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            print("Follow request already exists.")

    def get_follow_requests(self, username):
        response = self.follow_requests_table.query(
            KeyConditionExpression="following = :username",
            ExpressionAttributeValues={
                ":username": username
            }
        )
        requests = [item['follower'] for item in response['Items']]
        return requests

    def create_follow(self, follower, following):
        self.follow_table.put_item(
            Item={
                'follower': follower,
                'following': following
            }
        )

    def get_followings(self, username):
        response = self.follow_table.query(
            KeyConditionExpression="follower = :username",
            ExpressionAttributeValues={
                ":username": username
            }
        )
        followings = [item['following'] for item in response['Items']]
        return followings
