import boto3
import os
import json
import time
import uuid

class PostService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
        self.table_name = 'Posts'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f"Table '{self.table_name}' already exists. Loading it.")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[{'AttributeName': 'PostId', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'PostId', 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            print("Posts table created.")
        except Exception as e:
            raise RuntimeError(f"Error initializing DynamoDB table: {e}")

        self.posts_table = self.dynamodb.Table(self.table_name)
        self.s3 = boto3.client('s3', endpoint_url='http://localstack:4566')
        self.bucket_name = 'bandmates-media-storage'
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists.")
        except Exception as e:
            self.s3.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} created.")

    def create_post(self, post_id, description, content, username, timestamp):
        file_name = content.filename
        file_content = content.file
        unique_file_name = f"{post_id}_{file_name}"
        self.s3.put_object(Bucket=self.bucket_name, Key=unique_file_name, Body=file_content)
        url = f"http://localhost:4566/{self.bucket_name}/{unique_file_name}"

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
            created_post = {
                'PostId': post_id,
                'description': description,
                'url': url,
                'username': username,
                'Timestamp': timestamp
            }

            return created_post

        except Exception as e:
            raise RuntimeError(f"Error creating post: {e}")

    def get_post_by_id(self, post_id):
        try:
            response = self.posts_table.get_item(Key={'PostId': post_id})
            if 'Item' in response:
                return response['Item']
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Error retrieving post with post_id {post_id}: {e}")

    def clear_all_posts(self):
        try:
            response = self.posts_table.scan()
            items = response['Items']
            for item in items:
                self.posts_table.delete_item(Key={'PostId': item['PostId']})
            print("All posts deleted successfully.")
        except Exception as e:
            raise RuntimeError(f"Error clearing posts: {e}")

    def get_all_posts(self):
        try:
            response = self.posts_table.scan()
            items = response['Items']
            return items
        except Exception as e:
            raise RuntimeError(f"Error retrieving posts: {e}")
