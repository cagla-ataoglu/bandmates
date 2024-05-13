import boto3
from boto3.dynamodb.conditions import Key
import time
import decimal
import os

class GroupService:
    def __init__(self):
        """
            Initializes the GroupService class.
        """
        self.environment = os.getenv('ENV', 'development')
        self.dynamodb = self._get_dynamodb_resource()
        self.table_name = 'Groups'
        self.users_groups_table_name = 'UsersGroups'
        self.group_posts_table_name = 'GroupPosts'

        # Initialize Groups table
        self.initialize_table(self.table_name, 'GroupId')
        
        # Initialize UsersGroups table
        self.initialize_table(
            self.users_groups_table_name,
            'UserId',
            'GroupId',
            gsi={'name': 'GroupIdIndex', 'hash_key': 'GroupId'}
        )
        
        # Initialize GroupPosts table
        self.initialize_table(self.group_posts_table_name, 'GroupId', 'PostId')

        self.groups_table = self.dynamodb.Table(self.table_name)
        self.users_groups_table = self.dynamodb.Table(self.users_groups_table_name)
        self.group_posts_table = self.dynamodb.Table(self.group_posts_table_name)

    def _get_dynamodb_resource(self):
        """
            Retrieves the DynamoDB resource based on the environment. It defaults to 'development' but switches to 'test' if specified.
        """
        if self.environment == 'test':
            return boto3.resource('dynamodb')
        else:
            return boto3.resource('dynamodb', endpoint_url='http://localstack:4566')

    def initialize_table(self, table_name, hash_key, sort_key=None, gsi=None):
        """
            Initializes a DynamoDB table with specified attributes.

            Args:
                table_name: Name of the DynamoDB table.
                hash_key: Hash key attribute.
                sort_key: Sort key attribute (optional).
                gsi: Global Secondary Index details (optional).

            Raises:
                RuntimeError: If the table cannot be initialized.
        """
        try:
            table = self.dynamodb.Table(table_name)
            table.load()
            print(f"Table '{table_name}' already exists. Loading it.")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            key_schema = [{'AttributeName': hash_key, 'KeyType': 'HASH'}]
            attribute_definitions = [{'AttributeName': hash_key, 'AttributeType': 'S'}]
            if sort_key:
                key_schema.append({'AttributeName': sort_key, 'KeyType': 'RANGE'})
                attribute_definitions.append({'AttributeName': sort_key, 'AttributeType': 'S'})

            # Prepare GSI if specified
            gsi_definitions = []
            if gsi:
                gsi_definitions = [{
                    'IndexName': gsi['name'],
                    'KeySchema': [{'AttributeName': gsi['hash_key'], 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }]
                if 'sort_key' in gsi:
                    gsi_definitions[0]['KeySchema'].append({'AttributeName': gsi['sort_key'], 'KeyType': 'RANGE'})
                attribute_definitions.append({'AttributeName': gsi['hash_key'], 'AttributeType': 'S'})  # Adjust type as necessary
                if 'sort_key' in gsi:
                    attribute_definitions.append({'AttributeName': gsi['sort_key'], 'AttributeType': 'S'})  # Adjust type as necessary

            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
                GlobalSecondaryIndexes=gsi_definitions if gsi_definitions else None
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            print(f"Table '{table_name}' created.")
        except Exception as e:
            raise RuntimeError(f"Error initializing DynamoDB table '{table_name}': {e}")




    def create_group(self, group_id, group_name, description, user_id):
        """
            Creates a new group.

            Args:
                group_id: Unique identifier for the group.
                group_name: Name of the group.
                description: Description of the group.
                user_id: ID of the user creating the group.

            Raises:
                RuntimeError: If the group cannot be created.

            Returns:
                dict: The created group.
        """
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
        """
            Retrieves group details based on the group ID.

            Args:
                group_id: Unique identifier for the group.

            Raises:
                RuntimeError: If the group cannot be retrieved.

            Returns:
                dict: The group.
        """
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
        """
            Modifies the description of a group.

            Args:
                group_id: Unique identifier for the group.
                updated_description: New description for the group.

            Raises:
                RuntimeError: If the group description cannot be edited.
        """
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
        """
            Adds a user to a group.

            Args:
                user_id: ID of the user to be added.
                group_id: Unique identifier for the group.

            Raises:
                RuntimeError: If the user cannot be added to the group.
        """
        try:
            self.dynamodb.Table(self.users_groups_table_name).put_item(
                Item={'UserId': user_id, 'GroupId': group_id}
            )
            print('User added to group successfully.')
        except Exception as e:
            raise RuntimeError(f"Error adding user to group: {e}")

    def remove_user_from_group(self, user_id, group_id):
        """
            Removes a user from a group.

            Args:
                user_id: ID of the user to be removed.
                group_id: Unique identifier for the group.

            Raises:
                RuntimeError: If the user cannot be removed from the group.
        """
        try:
            self.dynamodb.Table(self.users_groups_table_name).delete_item(
                Key={'UserId': user_id, 'GroupId': group_id}
            )
            print('User removed from group successfully.')
        except Exception as e:
            raise RuntimeError(f"Error removing user from group: {e}")


    def get_group_members(self, group_id):
        """
            Retrieves members of a group.

            Args:
                group_id: Unique identifier for the group.

            Raises:
                RuntimeError: If the group members be retrieved.

            Returns:
                list: Members of the group.
        """
        try:
            # Querying the UsersGroups table using the GroupId as the key
            response = self.users_groups_table.query(
                IndexName='GroupIdIndex', 
                KeyConditionExpression=Key('GroupId').eq(group_id)
            )

            # Filtering user IDs from the response
            members = [item['UserId'] for item in response['Items']]
        
            return members
        except Exception as e:
            raise RuntimeError(f"Error retrieving group members for group {group_id}: {e}")


    def create_post(self, group_id, content, posted_by):
        """
            Creates a new post within a group.

            Args:
                group_id: Unique identifier for the group.
                content: Content of the post.
                posted_by: ID of the user posting the content.

            Raises:
                RuntimeError: If the post cannot be created.
        """
        try:
            timestamp = int(time.time() * 1000)
            self.dynamodb.Table(self.group_posts_table_name).put_item(
                Item={
                    'GroupId': group_id,
                    'PostId': str(timestamp),
                    'Content': content,
                    'PostedBy': posted_by,
                    'Timestamp': str(timestamp)
                }
            )
            print('Post created successfully.')
        except Exception as e:
            raise RuntimeError(f"Error creating post: {e}")

    def edit_post(self, group_id, post_id, updated_content):
        """
            Modifies the content of a post within a group.

            Args:
                group_id: Unique identifier for the group.
                post_id: Unique identifier for the post.
                updated_content: New content for the post.

            Raises:
                RuntimeError: If the post cannot be edited.
        """
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
        """
            Deletes a post within a group.

            Args:
                group_id: Unique identifier for the group.
                post_id: Unique identifier for the post.

            Raises:
                RuntimeError: If the post cannot be deleted.
        """
        try:
            self.dynamodb.Table(self.group_posts_table_name).delete_item(
                Key={'GroupId': group_id, 'PostId': post_id}
            )
            print('Post deleted successfully.')
        except Exception as e:
            raise RuntimeError(f"Error deleting post: {e}")


    def get_posts_in_group(self, group_id):
        """
            Retrieves all posts within a group.

            Args:
                group_id: Unique identifier for the group.

            Raises:
                RuntimeError: If the group posts cannot be retrieved.

            Returns:
                list: Posts in the group.
        """
        try:
            response = self.group_posts_table.query(
                KeyConditionExpression=Key('GroupId').eq(group_id)
            )
            return response['Items']
        except Exception as e:
            raise RuntimeError(f"Error retrieving posts for group {group_id}: {e}")
