import os
import unittest
from unittest.mock import patch
from moto import mock_dynamodb2, mock_s3
import boto3
from post_service import PostService
import io

# Mock environment variables
os.environ["AWS_ACCESS_KEY_ID"] = "fake_id"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_secret"
os.environ["AWS_SESSION_TOKEN"] = "fake_session_token"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["ENV"] = "test"

class TestPostService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_dynamodb = mock_dynamodb2()
        cls.mock_dynamodb.start()
        cls.mock_s3 = mock_s3()
        cls.mock_s3.start()

        # Create instance of the service
        cls.service = PostService()

    @classmethod
    def tearDownClass(cls):
        cls.mock_dynamodb.stop()
        cls.mock_s3.stop()

    def setUp(self):
        # Prepare a file-like object
        self.content = io.BytesIO(b"dummy image data")
        self.content.filename = "test_image.jpg"
        self.content.file = self.content  # Emulate Flask's FileStorage

    def test_create_post(self):
        post_id = "001"
        description = "Test post"
        username = "user1"
        timestamp = 1592208000

        # Test creating a post
        result = self.service.create_post(post_id, description, self.content, username, timestamp)
        self.assertIsNotNone(result)
        self.assertEqual(result['PostId'], post_id)
        self.assertEqual(result['description'], description)

    def test_get_post_by_id(self):
        post_id = "001"
        self.service.create_post(post_id, "Test post", self.content, "user1", 1592208000)
        
        # Test retrieving the post by ID
        post = self.service.get_post_by_id(post_id)
        self.assertIsNotNone(post)
        self.assertEqual(post['PostId'], post_id)

    def test_clear_all_posts(self):
        # Create multiple posts
        self.service.create_post("002", "Another Test Post", self.content, "user2", 1592211600)
        self.service.create_post("003", "Yet Another Test Post", self.content, "user3", 1592215200)

        # Clear all posts and verify
        self.service.clear_all_posts()
        posts = self.service.get_all_posts()
        self.assertEqual(len(posts), 0)

    def test_edit_post_description(self):
        post_id = "004"
        new_description = "Updated Description"
        self.service.create_post(post_id, "Old Description", self.content, "user4", 1592218800)

        # Update the post description
        self.service.edit_post_description(post_id, new_description)
        post = self.service.get_post_by_id(post_id)
        self.assertEqual(post['description'], new_description)

    def test_delete_post(self):
        post_id = "005"
        self.service.create_post(post_id, "Test Post to Delete", self.content, "user5", 1592222400)

        # Delete the post and verify
        self.service.delete_post(post_id)
        post = self.service.get_post_by_id(post_id)
        self.assertIsNone(post)

if __name__ == '__main__':
    unittest.main()
