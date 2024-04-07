import boto3

class GroupService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
        self.table_name = 'Groups'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f"Table '{self.table_name}' already exists. Loading it. Change test")
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



