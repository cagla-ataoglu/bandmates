import boto3
import json
import os

class DynamoDBService:
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

        self.table_name = 'Profiles'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f'Table {self.table_name} already exists. Loading it.')
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            table = self.dynamodb.create_table(
                TableName = self.table_name,
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
            table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
            print('Profiles table created.')
        except Exception as e:
            raise RuntimeError(f"Error initializing DynamoDB table: {e}")
        self.profiles_table = self.dynamodb.Table(self.table_name)

        self.bucket_name = 'profile-pictures-bucket'
        try:
            print('BEN BURADAYIM ilk')
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f'Bucket {self.bucket_name} exists.')
        except Exception as e:
            print('BEN BURADAYIM exception')
            self.s3.create_bucket(Bucket=self.bucket_name)
            print(f'Bucket {self.bucket_name} created.')
        

    def createMusicianProfile(self, username, display_name, location):
        profile_item = {
            'username': username,
            'display_name': display_name,
            'profile_type': 'musician',
            'location': location,
            'looking_for_gigs': False,
            'profile_picture': ''
        }

        self.profiles_table.put_item(Item=profile_item)
        print(f'Musician profile created for {username}.')

    def createBandProfile(self, username, display_name, location):
        profile_item = {
            'username': username,
            'display_name': display_name,
            'profile_type': 'band',
            'location': location,
            'looking_for_members': False,
            'profile_picture': ''
        }

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
            UpdateExpression='DELETE instruments :instrument',
            ConditionExpression='profile_type = :musician',
            ExpressionAttributeValues={
                ':instrument': set([instrument]),
                ':musician': 'musician'
            }
        )
        print(f'Instrument {instrument} removed from musician {username}.')

    def addMember(self, username, member):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='ADD members :member',
            ConditionExpression='profile_type = :band',
            ExpressionAttributeValues={
                ':member': set([member]),
                ':band': 'band'
            }
        )
        print(f'Member {member} added to band {username}.')

    def removeMember(self, username, member):
        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='DELETE members :member',
            ConditionExpression='profile_type = :band',
            ExpressionAttributeValues={
                ':member': set([member]),
                ':band': 'band'
            }
        )
        print(f'Member {member} removed from band {username}.')

    def updateLookingForGigs(self, username, state):
        state_bool = state.lower() == 'true'

        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='SET #looking_for_gigs = :state',
            ConditionExpression='profile_type = :musician',
            ExpressionAttributeNames={'#looking_for_gigs': 'looking_for_gigs'},
            ExpressionAttributeValues={
                ':state': state_bool,
                ':musician': 'musician'
            }
        )
        print(f'Looking for gigs set to {state_bool} for musician {username}.')

    def updateLookingForMembers(self, username, state):
        state_bool = state.lower() == 'true'

        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='SET #looking_for_members = :state',
            ConditionExpression='profile_type = :band',
            ExpressionAttributeNames={'#looking_for_members': 'looking_for_members'},
            ExpressionAttributeValues={
                ':state': state_bool,
                ':band': 'band'
            }
        )
        print(f'Looking for members set to {state_bool} for band {username}.')

    def updateProfilePicture(self, username, picture):
        file_name = f'{username}_{picture.filename}'
        file_content = picture.file
        self.s3.put_object(Bucket=self.bucket_name, Key=file_name, Body=file_content)
        url = self.url_base.format(bucket_name=self.bucket_name, key=file_name)

        response = self.profiles_table.update_item(
            Key={'username': username},
            UpdateExpression='SET #profile_picture = :profile_picture',
            ExpressionAttributeNames={'#profile_picture': 'profile_picture'},
            ExpressionAttributeValues={':profile_picture': url}
        )
        print(f'service: Profile picture updated for {username}.')

    def searchProfilesByUsernamePrefix(self, username_prefix, limit=7):
        response = self.profiles_table.scan(
            FilterExpression='begins_with(username, :prefix)',
            ExpressionAttributeValues={':prefix': username_prefix},
            Limit=limit
        )
        if 'Items' in response:
            return [sets_to_lists(item) for item in response['Items']]
        else:
            return []


def sets_to_lists(data):
    if isinstance(data, set):
        return list(data)
    elif isinstance(data, dict):
        return {key: sets_to_lists(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sets_to_lists(item) for item in data]
    else:
        return data
