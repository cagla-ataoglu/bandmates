import boto3
import os
import json
import time
import uuid

class PostService:
    def __init__(self):
        self.environment = os.getenv('ENV', 'development')
        if self.environment == 'production':
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
                KeySchema=[{'AttributeName': 'PostId', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'PostId', 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
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
        
    def delete_post(self, post_id):
        try:
            self.posts_table.delete_item(Key={'PostId': post_id})
            print(f'Post with id {post_id} deleted successfully.')
        except Exception as e:
            raise RuntimeError(f'Error deleting post with post_id {post_id}: {e}')
        
    def edit_post_description(self, post_id, new_description):
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
