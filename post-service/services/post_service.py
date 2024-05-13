import boto3
import os
import json
import time
import uuid

class PostService:
    def __init__(self):
        """
            Initializes PostService with the necessary resources and table.
        """
        self.environment = os.getenv('ENV', 'development')
        if self.environment == 'production':
            self.dynamodb = boto3.resource('dynamodb')
            self.s3 = boto3.client('s3')
            self.url_base = "https://{bucket_name}.s3.amazonaws.com/{key}"
        elif self.environment == 'test':
            self.dynamodb = boto3.resource('dynamodb')
            self.s3 = boto3.client('s3')
            self.url_base = "https://{bucket_name}.s3.amazonaws.com/{key}"
        else:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
            self.s3 = boto3.client('s3', endpoint_url='http://localstack:4566')
            self.url_base = "http://localhost:4566/{bucket_name}/{key}"

        self.table_name = 'Posts'
        self.bucket_name = 'bandmates-media-storage'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f"Table '{self.table_name}' already exists. Loading it.")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {'AttributeName': 'PostId', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'PostId', 'AttributeType': 'S'},
                    {'AttributeName': 'username', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5, 
                    'WriteCapacityUnits': 5
                },
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'UsernameIndex',
                        'KeySchema': [
                            {'AttributeName': 'username', 'KeyType': 'HASH'}
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5, 
                            'WriteCapacityUnits': 5
                        }
                    }
                ]
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            print("Posts table created.")
        except Exception as e:
            raise RuntimeError(f"Error initializing DynamoDB table: {e}")

        self.posts_table = self.dynamodb.Table(self.table_name)

        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists.")
        except Exception as e:
            self.s3.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} created.")

    def create_post(self, post_id, description, content, username, timestamp):
        """
            Creates a new post, uploads associated media content to S3, and stores metadata in DynamoDB.

            Args:
                post_id (str): The unique identifier for the post.
                description (str): The description of the post.
                content (FileStorage): The content file to be uploaded.
                username (str): The username of the user creating the post.
                timestamp (float): The timestamp of when the post was created.

            Returns:
                dict: Information about the created post.
        """
        file_name = content.filename
        file_content = content.file
        unique_file_name = f"{post_id}_{file_name}"
        self.s3.put_object(Bucket=self.bucket_name, Key=unique_file_name, Body=file_content)

        url = self.url_base.format(bucket_name=self.bucket_name, key=unique_file_name)

        try:
            self.posts_table.put_item(
                Item={
                    'PostId': post_id,
                    'description': description,
                    'url': url,
                    'username': username,
                    'Timestamp': timestamp
                }
            )
            print('Post created successfully.')
            return {
                'PostId': post_id,
                'description': description,
                'url': url,
                'username': username,
                'Timestamp': timestamp
            }
        except Exception as e:
            raise RuntimeError(f"Error creating post: {e}")

    def get_post_by_id(self, post_id):
        """
            Retrieves a post by its unique identifier.

            Args:
                post_id (str): The unique identifier of the post.

            Returns:
                dict or None: Information about the retrieved post, or None if not found.
        """
        try:
            response = self.posts_table.get_item(Key={'PostId': post_id})
            if 'Item' in response:
                return response['Item']
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Error retrieving post with post_id {post_id}: {e}")

    def clear_all_posts(self):
        """
            Clears all posts from the DynamoDB table.
        """
        try:
            response = self.posts_table.scan()
            items = response['Items']
            for item in items:
                self.posts_table.delete_item(Key={'PostId': item['PostId']})
            print("All posts deleted successfully.")
        except Exception as e:
            raise RuntimeError(f"Error clearing posts: {e}")

    def get_posts_by_usernames(self, usernames):
        """
            Retrieves all posts by the given list of usernames.

            Args:
                usernames (list): List of usernames.

            Returns:
                list: List of posts by the given usernames, sorted by timestamp.
        """
        all_posts = []
        for username in usernames:
            try:
                response = self.posts_table.query(
                    IndexName='UsernameIndex',
                    KeyConditionExpression=boto3.dynamodb.conditions.Key('username').eq(username)
                )
                posts = response.get('Items', [])
                all_posts.extend(posts)
            except Exception as e:
                raise RuntimeError(f"Error retrieving posts for username {username}: {e}")
        
        all_posts_sorted = sorted(all_posts, key=lambda post: post['Timestamp'])
        return all_posts_sorted

    def get_all_posts(self):
        """
            Retrieves all posts from the DynamoDB table.

            Returns:
                list: List of all posts.
        """
        try:
            response = self.posts_table.scan()
            items = response['Items']
            return items
        except Exception as e:
            raise RuntimeError(f"Error retrieving posts: {e}")
        
    def delete_post(self, post_id):
        """
            Deletes a post with the given post_id.

            Args:
                post_id (str): The unique identifier of the post.
        """
        try:
            self.posts_table.delete_item(Key={'PostId': post_id})
            print(f'Post with id {post_id} deleted successfully.')
        except Exception as e:
            raise RuntimeError(f'Error deleting post with post_id {post_id}: {e}')
        
    def edit_post_description(self, post_id, new_description):
        """
            Edits the description of a post.

            Args:
                post_id (str): The unique identifier of the post.
                new_description (str): The new description for the post.
        """
        try:
            self.posts_table.update_item(
            Key={'PostId': post_id},
            UpdateExpression='SET #description = :new_description',
            ExpressionAttributeNames={'#description': 'description'},
            ExpressionAttributeValues={':new_description': new_description}
        )
            print(f'Description of post with id {post_id} updated successfully.')
        except Exception as e:
            raise RuntimeError(f'Error editing description of post with post_id {post_id}: {e}')
