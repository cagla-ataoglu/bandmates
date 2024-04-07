import boto3

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

    def create_post(self, post_id, content, user_id, timestamp):
        try:
            self.posts_table.put_item(
                Item={
                    'PostId': post_id,
                    'Content': content,
                    'UserId': user_id,
                    'Timestamp': timestamp
                }
            )
            print('Post created successfully.')
            created_post = {
                'PostId': post_id,
                'Content': content,
                'UserId': user_id,
                'Timestamp': timestamp
            }
            
            return created_post
            
        except Exception as e:
            raise RuntimeError(f"Error creating post: {e}")

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
