import boto3
import os
from datetime import datetime, timezone
import uuid

class MessageService:
    def __init__(self):
        self.environment = os.getenv('ENV', 'development')
        if self.environment == 'production' or self.environment == 'test':
            self.dynamodb = boto3.resource('dynamodb')
        else:
            self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')

        self.chats_table_name = 'Chats'
        self.chat_members_table_name = 'ChatMembers'
        self.messages_table_name = 'Messages'

        self.chat_table = self.ensure_table(self.chats_table_name)
        self.chat_members_table = self.ensure_table(self.chat_members_table_name, members=True)
        self.messages_table = self.ensure_table(self.messages_table_name, messages=True)

    def ensure_table(self, table_name, members=False, messages=False):
        try:
            table = self.dynamodb.Table(table_name)
            table.load()
            print(f'Table {table_name} already exists. Loading it.')
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            if members:
                table = self.dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {'AttributeName': 'chat_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'username', 'KeyType': 'RANGE'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'chat_id', 'AttributeType': 'S'},
                        {'AttributeName': 'username', 'AttributeType': 'S'}
                    ],
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'UserChatsIndex',
                            'KeySchema': [{'AttributeName': 'username', 'KeyType': 'HASH'}],
                            'Projection': {'ProjectionType': 'INCLUDE', 'NonKeyAttributes': ['chat_id']},
                            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                        }
                    ],
                    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                )
            elif messages:
                table = self.dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {'AttributeName': 'chat_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'message_id', 'KeyType': 'RANGE'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'chat_id', 'AttributeType': 'S'},
                        {'AttributeName': 'message_id', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                )
            else:
                table = self.dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {'AttributeName': 'chat_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'chat_name', 'KeyType': 'RANGE'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'chat_id', 'AttributeType': 'S'},
                        {'AttributeName': 'chat_name', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                )
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            print(f'{table_name} table created.')
        return table

    def create_chat(self, usernames, chat_name, is_group=False):
        chat_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        for username in usernames:
            self.chat_members_table.put_item(
                Item={
                    'chat_id': chat_id,
                    'username': username
                }
            )
        self.chat_table.put_item(
            Item={
                'chat_id': chat_id,
                'chat_name': chat_name,
                'is_group': is_group,
                'usernames': usernames,
                'created_at': timestamp
            }
        )
        return chat_id

    def send_message(self, chat_id, username, message):
        message_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        self.messages_table.put_item(
            Item={
                'chat_id': chat_id,
                'message_id': message_id,
                'username': username,
                'message': message,
                'timestamp': timestamp
            }
        )
        print("Message sent successfully.")

    def get_user_chats(self, username):
        response = self.chat_members_table.query(
            IndexName='UserChatsIndex',
            KeyConditionExpression="username = :username",
            ExpressionAttributeValues={":username": username},
            ScanIndexForward=False
        )
        return response['Items']

    def get_messages(self, chat_id):
        response = self.messages_table.query(
            KeyConditionExpression="chat_id = :chat_id",
            ExpressionAttributeValues={":chat_id": chat_id}
        )
        sorted_messages = sorted(response['Items'], key=lambda x: x['timestamp'])
        return sorted_messages
