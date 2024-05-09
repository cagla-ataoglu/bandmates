import unittest
from moto import mock_aws
import boto3
import time
from group_service import GroupService
import os
from unittest.mock import patch

class TestGroupService(unittest.TestCase):

    @patch('group_service.GroupService._get_dynamodb_resource')
    def setUp(self, mock_get_dynamodb_resource):
        """Set up the mock DynamoDB tables and initialize GroupService."""
        # Mocking the DynamoDB resource
        mock_dynamodb_resource = mock_get_dynamodb_resource.return_value
        
        # Creating mock tables
        self.mock_groups_table = mock_dynamodb_resource.Table.return_value
        self.mock_users_groups_table = mock_dynamodb_resource.Table.return_value
        self.mock_group_posts_table = mock_dynamodb_resource.Table.return_value
        
        # Initializing GroupService
        self.group_service = GroupService()

    def test_create_group(self):
        group_id = 'test-group-1'
        group_name = 'Test Group'
        description = 'A test group'
        user_id = 'test-user-1'

        created_group = self.group_service.create_group(group_id, group_name, description, user_id)
        self.assertEqual(created_group['GroupId'], group_id)
        self.assertEqual(created_group['GroupName'], group_name)
        self.assertEqual(created_group['Description'], description)
        self.assertEqual(created_group['CreatorUserId'], user_id)

        fetched_group = self.group_service.get_group(group_id)
        self.assertEqual(fetched_group['GroupId'], group_id)
        self.assertEqual(fetched_group['GroupName'], group_name)
        self.assertEqual(fetched_group['Description'], description)
        self.assertEqual(fetched_group['CreatorUserId'], user_id)

    def test_edit_group_description(self):
        group_id = 'test-group-2'
        self.group_service.create_group(group_id, 'Group to Edit', 'Old Description', 'user-2')

        new_description = 'Updated Description'
        self.group_service.edit_group_description(group_id, new_description)

        edited_group = self.group_service.get_group(group_id)
        self.assertEqual(edited_group['Description'], new_description)

    def test_add_and_remove_user_from_group(self):
        user_id = 'test-user-2'
        group_id = 'test-group-3'
        self.group_service.create_group(group_id, 'Another Group', 'Some Description', 'user-3')

        self.group_service.add_user_to_group(user_id, group_id)
        members = self.group_service.get_group_members(group_id)
        print("Members from: " + str(members))
        self.assertIn(user_id, members)

        self.group_service.remove_user_from_group(user_id, group_id)
        members = self.group_service.get_group_members(group_id)
        self.assertNotIn(user_id, members)

    def test_create_and_edit_post(self):
        group_id = 'test-group-4'
        self.group_service.create_group(group_id, 'Group for Posts', 'Post Description', 'user-4')
        content = 'Initial Post Content'
        posted_by = 'user-4'

        timestamp = int(time.time() * 1000)
        post_id = str(timestamp)
        self.group_service.create_post(group_id, content, posted_by)

        posts = self.group_service.get_posts_in_group(group_id)
        self.assertEqual(posts[0]['Content'], content)
        self.assertEqual(posts[0]['PostedBy'], posted_by)

        updated_content = 'Updated Post Content'
        self.group_service.edit_post(group_id, post_id, updated_content)
        posts = self.group_service.get_posts_in_group(group_id)
        self.assertEqual(posts[0]['Content'], updated_content)

    def test_delete_post(self):
        group_id = 'test-group-5'
        self.group_service.create_group(group_id, 'Group for Deletion', 'Deletion Group', 'user-5')
        content = 'Content to be Deleted'
        posted_by = 'user-5'

        timestamp = int(time.time() * 1000)
        post_id = str(timestamp)
        self.group_service.create_post(group_id, content, posted_by)

        posts = self.group_service.get_posts_in_group(group_id)
        self.assertEqual(posts[0]['PostId'], post_id)

        self.group_service.delete_post(group_id, post_id)
        posts = self.group_service.get_posts_in_group(group_id)
        self.assertEqual(len(posts), 0)

if __name__ == '__main__':
    unittest.main()
