import os
import unittest
from unittest.mock import patch
from moto import mock_dynamodb2, mock_s3
import boto3
from post_service import PostService
import io

# Setting environment variables for mocked AWS services
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

class TestPostService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup mocked AWS services for all tests in this suite."""
        cls.mock_dynamodb2 = mock_dynamodb2()
        cls.mock_dynamodb2.start()
        cls.mock_s3 = mock_s3()
        cls.mock_s3.start()
        # Patch boto3 resource and client to use moto's mocks by default
        cls.patcher_resource = patch('boto3.resource', boto3.resource)
        cls.patcher_client = patch('boto3.client', boto3.client)
        cls.mock_resource = cls.patcher_resource.start()
        cls.mock_client = cls.patcher_client.start()

        # Ensure the service uses the mocked boto3
        cls.service = PostService()

    @classmethod
    def tearDownClass(cls):
        """Stop all patches and moto mocks."""
        cls.mock_dynamodb2.stop()
        cls.mock_s3.stop()
        cls.patcher_resource.stop()
        cls.patcher_client.stop()

    def test_create_post(self):
        post_id = '001'
        description = 'A new post'
        content = io.BytesIO(b'Test content')
        content.filename = 'test.jpg'
        username = 'testuser'
        timestamp = 1234567890

        created_post = self.service.create_post(post_id, description, content, username, timestamp)

        # Assertions to verify the contents of the created post
        self.assertEqual(created_post['PostId'], post_id)
        self.assertEqual(created_post['description'], description)
        self.assertIn('http://localhost:4566/bandmates-media-storage/001_test.jpg', created_post['url'])
        self.assertEqual(created_post['username'], username)
        self.assertEqual(created_post['Timestamp'], timestamp)

    def test_get_post_by_id(self):
        post_id = '002'
        description = 'Another post'
        content = io.BytesIO(b'More test content')
        content.filename = 'another.jpg'
        username = 'user2'
        timestamp = 9876543210
        self.service.create_post(post_id, description, content, username, timestamp)

        # Retrieve the post
        retrieved_post = self.service.get_post_by_id(post_id)

        # Check that the retrieved post matches what was created
        self.assertIsNotNone(retrieved_post)
        self.assertEqual(retrieved_post['PostId'], post_id)

    def test_clear_all_posts(self):
        # Create multiple posts as setup
        self.service.create_post('003', 'Post Three', io.BytesIO(b'Content three'), 'user3', 1111111111)
        self.service.create_post('004', 'Post Four', io.BytesIO(b'Content four'), 'user4', 2222222222)

        # Clear all posts
        self.service.clear_all_posts()

        # Verify that no posts remain
        all_posts = self.service.get_all_posts()
        self.assertEqual(len(all_posts), 0)

    def test_get_all_posts(self):
        # Create multiple posts
        self.service.create_post('005', 'Post Five', io.BytesIO(b'Content five'), 'user5', 3333333333)
        self.service.create_post('006', 'Post Six', io.BytesIO(b'Content six'), 'user6', 4444444444)

        # Retrieve all posts
        all_posts = self.service.get_all_posts()

        # Verify that all posts are retrieved
        self.assertEqual(len(all_posts), 2)

if __name__ == "__main__":
    unittest.main()
