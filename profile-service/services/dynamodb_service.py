import boto3

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
        self.table_name = 'Profiles'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f'Table {self.table_name} already exists. Loading it.')
        except Exception as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                table = self.dynamodb.create_table(
                    TableName = 'Profiles',
                    KeySchema = [{
                        'AttributeName': 'username',
                        'KeyType': 'HASH'
                    }],
                    AttributeDefinitions = [{
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    }],
                    ProvisionedThroughput = {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                table.meta.client.get_waiter('table_exists').wait(TableName='Profiles')
                print('Profiles table created.')
            else:
                raise
        self.profiles_table = self.dynamodb.Table('Profiles')

    def createMusicianProfile(self, username, display_name, instruments, genres, location):
        profile_item = {
            'username': username,
            'display_name': display_name,
            'profile_type': 'musician',
            'instruments': instruments,
            'genres': genres,
            'location': location
        }

        self.profiles_table.put_item(Item=profile_item)
        print(f'Musician profile created for {username}.')

    def createBandProfile(self, username, display_name, members, genres, location):
        profile_item = {
            'username': username,
            'display_name': display_name,
            'profile_type': 'band',
            'members': members,
            'genres': genres,
            'location': location
        }

        self.profiles_table.put_item(Item=profile_item)
        print(f'Band profile created for {username}.')

    def getProfile(self, username):
        response = self.profiles_table.get_item(Key={'username': username})
        if 'Item' in response:
            return response['Item']
        else:
            print(f'No profile found for {username}.')
            return None
        
    def updateDisplayName(self, username, new_display_name):
        try:
            response = self.profiles_table.update_item(
                Key={'username': username},
                UpdateExpression='SET #display_name = :display_name',
                ExpressionAttributeNames={'#display_name': 'display_name'},
                ExpressionAttributeValues={':display_name': new_display_name}
            )
            print(f'Display name updated for {username} to {new_display_name}')
        except Exception as e:
            print(f'Error updating display name for {username}: {e}')
