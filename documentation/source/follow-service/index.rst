Follow Service
==============

.. code:: python

    import boto3
    import json
    import os

    class FollowService:
        """
        FollowService is a class to manage follow requests and follow relations
        between users in a social media platform.

        Attributes:
            environment (str): The environment in which the service is running. Default is 'development'.
            dynamodb (boto3.resource): The DynamoDB resource.
            follow (str): The name of the main follow table.
            follow_requests (str): The name of the follow requests table.
            follow_table (boto3.resource.Table): The DynamoDB table for follows.
            follow_requests_table (boto3.resource.Table): The DynamoDB table for follow requests.
        """

        def __init__(self):
            """
            Initializes FollowService with the necessary resources and tables.
            """
            self.environment = os.getenv('ENV', 'development')
            if self.environment == 'production' or self.environment == 'test':
                self.dynamodb = boto3.resource('dynamodb')
            else:
                self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')

            self.follow = 'Follow'
            self.follow_requests = 'Follow_requests'

            self.follow_table = self.ensure_follow_table(self.follow)
            self.follow_requests_table = self.ensure_follow_table(self.follow_requests)

        def ensure_follow_table(self, table_name):
            """
            Ensures that the specified DynamoDB table exists, otherwise creates it.

            Args:
                table_name (str): The name of the table to ensure.

            Returns:
                boto3.resource.Table: The DynamoDB table.
            """
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
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'FollowingIndex',
                            'KeySchema': [
                                {
                                    'AttributeName': 'following',
                                    'KeyType': 'HASH'
                                },
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL'
                            },
                            'ProvisionedThroughput': {
                                'ReadCapacityUnits': 5,
                                'WriteCapacityUnits': 5
                            }
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
            """
            Sends a follow request from one user to another.

            Args:
                follower (str): The username of the user sending the request.
                following (str): The username of the user to whom the request is sent.
            """
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
            """
            Retrieves follow requests for a user.

            Args:
                username (str): The username of the user.

            Returns:
                list: A list of usernames who sent follow requests.
            """
            response = self.follow_requests_table.query(
                KeyConditionExpression="following = :username",
                ExpressionAttributeValues={
                    ":username": username
                }
            )
            requests = [item['follower'] for item in response['Items']]
            return requests

        def create_follow(self, follower, following):
            """
            Creates a follow relation between two users.

            Args:
                follower (str): The username of the follower.
                following (str): The username of the user being followed.
            """
            self.follow_table.put_item(
                Item={
                    'follower': follower,
                    'following': following
                }
            )
        
        def delete_follow(self, follower, following):
            """
            Deletes a follow relation between two users.

            Args:
                follower (str): The username of the follower.
                following (str): The username of the user being followed.
            """
            self.follow_table.delete_item(
                Key={
                    'follower': follower,
                    'following': following
                }
            )

        def get_followings(self, username):
            """
            Retrieves users that a given user is following.

            Args:
                username (str): The username of the user.

            Returns:
                list: A list of usernames being followed by the given user.
            """
            response = self.follow_table.query(
                KeyConditionExpression="follower = :username",
                ExpressionAttributeValues={
                    ":username": username
                }
            )
            followings = [item['following'] for item in response['Items']]
            return followings

        def get_followers(self, username):
            """
            Retrieves users who are following a given user.

            Args:
                username (str): The username of the user.

            Returns:
                list: A list of usernames who are following the given user.
            """
            response = self.follow_table.query(
                IndexName='FollowingIndex',  # Specify the correct GSI name
                KeyConditionExpression="following = :username",
                ExpressionAttributeValues={
                    ":username": username
                }
            )
            followers = [item['follower'] for item in response['Items']]
            return followers
