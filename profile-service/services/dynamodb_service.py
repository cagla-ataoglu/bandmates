import boto3
import json

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
            'location': location
        }

        if genres:
            profile_item['genres'] = genres

        if instruments:
            profile_item['instruments'] = instruments

        self.profiles_table.put_item(Item=profile_item)
        print(f'Musician profile created for {username}.')

    def createBandProfile(self, username, display_name, members, genres, location):
        profile_item = {
            'username': username,
            'display_name': display_name,
            'profile_type': 'band',
            'members': members,
            'location': location
        }

        if genres:
            profile_item['genres'] = genres 

        self.profiles_table.put_item(Item=profile_item)
        print(f'Band profile created for {username}.')

    def getProfile(self, username):
        response = self.profiles_table.get_item(Key={'username': username})
        if 'Item' in response:
            return sets_to_lists(response['Item'])
        else:
            print(f'No profile found for {username}.')
            return None
        
    def updateDisplayName(self, username, new_display_name):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='SET #display_name = :display_name',
            ExpressionAttributeNames={'#display_name': 'display_name'},
            ExpressionAttributeValues={':display_name': new_display_name}
        )
        print(f'Display name updated for {username} to {new_display_name}.')

    def updateLocation(self, username, new_location):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='SET #location = :location',
            ExpressionAttributeNames={'#location': 'location'},
            ExpressionAttributeValues={':location': new_location}
        )
        print(f'Location updated for {username} to {new_location}.')

    def addGenre(self, username, genre):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='ADD genres :genre',
            ExpressionAttributeValues={':genre': set([genre])}
        )
        print(f'Genre {genre} added to {username}.')

    def removeGenre(self, username, genre):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='DELETE genres :genre',
            ExpressionAttributeValues={':genre': set([genre])}
        )
        print(f'Genre {genre} removed from {username}.')

    def addInstrument(self, username, instrument):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='ADD instruments :instrument',
            ConditionExpression='profile_type = :musician',
            ExpressionAttributeValues={
                ':instrument': set([instrument]),
                ':musician': 'musician'
            }
        )
        print(f'Instrument {instrument} added to musician {username}.')

    def removeInstrument(self, username, instrument):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='DELERE instruments :instrument',
            ConditionExpression='profile_type = :musician',
            ExpressionAttributeValues={
                ':instrument': set([instrument]),
                ':musician': 'musician'
            }
        )
        print(f'Instrument {instrument} removed from musician {username}.')

def sets_to_lists(data):
    if isinstance(data, set):
        return list(data)
    elif isinstance(data, dict):
        return {key: sets_to_lists(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sets_to_lists(item) for item in data]
    else:
        return data
