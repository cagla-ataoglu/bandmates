import boto3
from boto3.dynamodb.types import TypeSerializer

class GroupService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
        self.table_name = 'Groups'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f"Table '{self.table_name}' already exists. Loading it.")
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[{'AttributeName': 'GroupId', 'KeyType': 'HASH'}],
                AttributeDefinitions=[{'AttributeName': 'GroupId', 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            print("Groups table created.")
        except Exception as e:
            raise RuntimeError(f"Error initializing DynamoDB table: {e}")

        self.groups_table = self.dynamodb.Table(self.table_name)

    def create_group(self, group_id, group_name, description, user_id):
        try:
            self.groups_table.put_item(
                Item={
                    'GroupId': serializer.serialize(group_id),
                    'GroupName': serializer.serialize(group_name),
                    'Description': serializer.serialize(description),
                    'CreatorUserId': serializer.serialize(user_id)
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
            raise RuntimeError(f"Error creating group: {e}")

    def get_group(self, user_id):
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

    #def add_user(self, user_id, group_id):
    #    try:
    #        group: self.get_group(group_id)
    #        if group:
    #            group['Members'] 



