import os
import boto3
import unittest
from moto import mock_dynamodb2
from group_service import GroupService
import time

"""Mocked AWS Credentials for moto."""
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["ENV"] = "test"

@mock_dynamodb2
def set_up():
    with mock_dynamodb2():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        # Create Groups table
        dynamodb.create_table(
            TableName='Groups',
            KeySchema=[{'AttributeName': 'GroupId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'GroupId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # Create UsersGroups table
        dynamodb.create_table(
            TableName='UsersGroups',
            KeySchema=[{'AttributeName': 'UserId', 'KeyType': 'HASH'}, {'AttributeName': 'GroupId', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[{'AttributeName': 'UserId', 'AttributeType': 'S'}, {'AttributeName': 'GroupId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
            GlobalSecondaryIndexes=[{
                'IndexName': 'GroupIdIndex',
                'KeySchema': [{'AttributeName': 'GroupId', 'KeyType': 'HASH'}],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            }]
        )

        # Create GroupPosts table
        dynamodb.create_table(
            TableName='GroupPosts',
            KeySchema=[{'AttributeName': 'GroupId', 'KeyType': 'HASH'}, {'AttributeName': 'PostId', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[{'AttributeName': 'GroupId', 'AttributeType': 'S'}, {'AttributeName': 'PostId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # Wait for the tables to be ready
        time.sleep(2)

        return GroupService()

@mock_dynamodb2
def test_create_group():
    group_service = set_up()
    group_id = 'test_group_id'
    group_name = 'Test Group'
    description = 'This is a test group'
    user_id = 'test_user_id'
    created_group = group_service.create_group(group_id, group_name, description, user_id)
    assert created_group['GroupId'] == group_id
    assert created_group['GroupName'] == group_name
    assert created_group['Description'] == description
    assert created_group['CreatorUserId'] == user_id

@mock_dynamodb2
def test_get_group():
    group_service = set_up()
    group_id = 'test_group_id'
    group_name = 'Test Group'
    description = 'This is a test group'
    user_id = 'test_user_id'
    group_service.create_group(group_id, group_name, description, user_id)
    group = group_service.get_group(group_id)
    assert group is not None
    assert group['GroupId'] == group_id

@mock_dynamodb2
def test_edit_group_description():
    group_service = set_up()
    group_id = 'test_group_id'
    group_name = 'Test Group'
    description = 'This is a test group'
    user_id = 'test_user_id'
    group_service.create_group(group_id, group_name, description, user_id)
    updated_description = 'Updated Description'
    group_service.edit_group_description(group_id, updated_description)
    group = group_service.get_group(group_id)
    assert group['Description'] == updated_description

@mock_dynamodb2
def test_add_user_to_group():
    group_service = set_up()
    group_id = 'test_group_id'
    user_id = 'test_user_id'
    group_service.create_group(group_id, 'Test Group', 'Description', user_id)
    group_service.add_user_to_group(user_id, group_id)
    members = group_service.get_group_members(group_id)
    assert user_id in members

@mock_dynamodb2
def test_remove_user_from_group():
    group_service = set_up()
    group_id = 'test_group_id'
    user_id = 'test_user_id'
    group_service.create_group(group_id, 'Test Group', 'Description', user_id)
    group_service.add_user_to_group(user_id, group_id)
    group_service.remove_user_from_group(user_id, group_id)
    members = group_service.get_group_members(group_id)
    assert user_id not in members

@mock_dynamodb2
def test_create_post():
    group_service = set_up()
    group_id = 'test_group_id'
    group_service.create_group(group_id, 'Test Group', 'Description', 'test_user_id')
    group_service.create_post(group_id, 'This is a test post', 'test_user_id')
    posts = group_service.get_posts_in_group(group_id)
    assert len(posts) == 1
    assert posts[0]['Content'] == 'This is a test post'

if __name__ == "__main__":
    pytest.main()
