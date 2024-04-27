import json
import boto3
import os

def lambda_handler(event, context):
    # Initialize DynamoDB
    dynamodb = boto3.resource('dynamodb', endpoint_url=os.getenv())
    profiles_table = dynamodb.Table(os.getenv('PROFILES_TABLE'))

    # Parse the incoming JSON payload from API Gateway
    try:
        data = json.loads(event['body'])
        username = data.get('username')
        if not username:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Username is required.'})
            }
        
        display_name = data.get('display_name')
        location = data.get('location')

        # Prepare the item to put into the DynamoDB table
        profile_item = {
            'username': username,
            'display_name': display_name,
            'profile_type': 'musician',
            'location': location
        }

        # Insert item into DynamoDB
        profiles_table.put_item(Item=profile_item)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Musician profile created for {username}.'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
