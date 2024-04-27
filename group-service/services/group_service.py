import boto3
from boto3.dynamodb.conditions import Key
import time

class GroupService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
        self.table_name = 'Groups'
        self.users_groups_table_name = 'UsersGroups'
        self.group_posts_table_name = 'GroupPosts'

        # Initialize Groups table
        self.initialize_table(self.table_name, 'GroupId')
        
        # Initialize UsersGroups table
        self.initialize_table(self.users_groups_table_name, 'UserId', 'GroupId')
        
        # Initialize GroupPosts table
        self.initialize_table(self.group_posts_table_name, 'GroupId', 'PostId')

    def initialize_table(self, table_name, hash_key, sort_key=None):
        try:
            self.dynamodb.Table(table_name).load()
            print(f"Table '{table_name}' already exists. Loading it.")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            key_schema = [{'AttributeName': hash_key, 'KeyType': 'HASH'}]
            attribute_definitions = [{'AttributeName': hash_key, 'AttributeType': 'S'}]
            if sort_key:
                key_schema.append({'AttributeName': sort_key, 'KeyType': 'RANGE'})
                attribute_definitions.append({'AttributeName': sort_key, 'AttributeType': 'S'})
            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            print(f"Table '{table_name}' created.")
        except Exception as e:
            raise RuntimeError(f"Error initializing DynamoDB table '{table_name}': {e}")


    def create_group(self, group_id, group_name, description, user_id):
        try:
            print("Creating group with the following attributes:")
            print(f"Group ID: {group_id}")
            print(f"Group Name: {group_name}")
            print(f"Description: {description}")
            print(f"Creator User ID: {user_id}")
            self.groups_table.put_item(
                Item={
                    'GroupId': str(group_id),
                    'GroupName': str(group_name),
                    'Description': str(description),
                    'CreatorUserId': str(user_id)
                }
            )
            print('Group created successfully.')
            created_group = {
            'GroupId': group_id,
            'GroupName': group_name,
            'Description': description,
            'CreatorUserId': user_id
            }
            
            return created_group
        
        except Exception as e:
            raise RuntimeError(f"Error creating group: {e} Change test ")

    def get_group(self, group_id):
        try:
            response = self.groups_table.query(
                 KeyConditionExpression=Key('GroupId').eq(group_id),
                 ScanIndexForward=False,  
                 Limit=1  
             )
            items = response['Items']
            if items:
                return items[0]
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Error retrieving group: {e}")
        
    def edit_group_description(self, group_id, updated_description):
        try:
            group = self.get_group(group_id)
            if group:
                group['Description'] = updated_description
                self.groups_table.put_item(Item=group)
                print('Group description edited successfully.')
            else:
                print('Group not found.')
        except Exception as e:
            raise RuntimeError(f"Error editing group description: {e}")


    def add_user_to_group(self, user_id, group_id):
        try:
            self.dynamodb.Table(self.users_groups_table_name).put_item(
                Item={'UserId': user_id, 'GroupId': group_id}
            )
            print('User added to group successfully.')
        except Exception as e:
            raise RuntimeError(f"Error adding user to group: {e}")

    def remove_user_from_group(self, user_id, group_id):
        try:
            self.dynamodb.Table(self.users_groups_table_name).delete_item(
                Key={'UserId': user_id, 'GroupId': group_id}
            )
            print('User removed from group successfully.')
        except Exception as e:
            raise RuntimeError(f"Error removing user from group: {e}")


    def get_group_members(self, group_id):
        try:
            # Setting up the table
            users_groups_table = self.dynamodb.Table(self.users_groups_table_name)
        
            # Querying the UsersGroups table using the GroupId as the key
            response = users_groups_table.query(
                IndexName='GroupIdIndex',  # Ensure this GSI is setup in your table
                KeyConditionExpression=Key('GroupId').eq(group_id)
            )
        
            # Extracting user IDs from the response
            members = [item['UserId'] for item in response['Items']]
        
            return members
        except Exception as e:
            raise RuntimeError(f"Error retrieving group members for group {group_id}: {e}")


    def create_post(self, group_id, content, posted_by):
        try:
            timestamp = int(time.time() * 1000)
            self.dynamodb.Table(self.group_posts_table_name).put_item(
                Item={
                    'GroupId': group_id,
                    'PostId': str(timestamp),
                    'Content': content,
                    'PostedBy': posted_by,
                    'Timestamp': timestamp
                }
            )
            print('Post created successfully.')
        except Exception as e:
            raise RuntimeError(f"Error creating post: {e}")

    def edit_post(self, group_id, post_id, updated_content):
        try:
            # Get the current post to check it exists
            response = self.dynamodb.Table(self.group_posts_table_name).get_item(
                Key={'GroupId': group_id, 'PostId': post_id}
            )
            post = response.get('Item')
            if not post:
                print('Post not found.')
                return
        
            # Update the post content
            post['Content'] = updated_content
            self.dynamodb.Table(self.group_posts_table_name).put_item(Item=post)
            print('Post edited successfully.')
        except Exception as e:
            raise RuntimeError(f"Error editing post: {e}")

    
    def delete_post(self, group_id, post_id):
        try:
            self.dynamodb.Table(self.group_posts_table_name).delete_item(
                Key={'GroupId': group_id, 'PostId': post_id}
            )
            print('Post deleted successfully.')
        except Exception as e:
            raise RuntimeError(f"Error deleting post: {e}")

    
    def get_posts_in_group(self, group_id):
        try:
            response = self.group_posts_table.query(
                KeyConditionExpression=Key('GroupId').eq(group_id)
            )
            return response['Items']
        except Exception as e:
            raise RuntimeError(f"Error retrieving posts for group {group_id}: {e}")
