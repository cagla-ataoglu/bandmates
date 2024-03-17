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

    def create_post(self, post_id, title, content, user_id, timestamp, video_url):
        try:
            self.posts_table.put_item(
                Item={
                    'PostId': post_id,
                    'Title': title,
                    'Content': content,
                    'UserId': user_id,
                    'Timestamp': timestamp,
                    'VideoUrl': video_url
                }
            )
            print('Post created successfully.')
        except Exception as e:
            raise RuntimeError(f"Error creating post: {e}")

    def get_post(self, post_id):
        try:
            response = self.posts_table.get_item(Key={'PostId': post_id})
            if 'Item' in response:
                return response['Item']
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Error retrieving post: {e}")
        
    def edit_post(self, post_id, updated_content):
        try:
            post = self.get_post(post_id)
            if post:
                post['Content'] = updated_content
                self.posts_table.put_item(Item=post)
                print('Post edited successfully.')
            else:
                print('Post not found.')
        except Exception as e:
            raise RuntimeError(f"Error editing post: {e}")

