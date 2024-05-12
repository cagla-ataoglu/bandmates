import unittest
from unittest.mock import patch
from moto import mock_dynamodb2
import boto3
import os
from follow_service import FollowService

# Mock environment variables
os.environ["AWS_ACCESS_KEY_ID"] = "fake_id"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_secret"
os.environ["AWS_SESSION_TOKEN"] = "fake_session_token"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["ENV"] = "test"

class TestFollowService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup mocked DynamoDB for all tests."""
        cls.mock = mock_dynamodb2()
        cls.mock.start()
        cls.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        cls.original_env = os.getenv('ENV')
        os.environ['ENV'] = 'test'

        cls.service = FollowService()

    @classmethod
    def tearDownClass(cls):
        """Stop all mocks and reset the environment variable."""
        cls.mock.stop()
        if cls.original_env is not None:
            os.environ['ENV'] = cls.original_env
        else:
            del os.environ['ENV']

    def test_send_follow_request(self):
        """Test sending a follow request."""
        # Send a follow request
        self.service.send_follow_request('follower1', 'following1')
        
        # Check if the follow request is sent successfully
        print("Follow requests:", self.service.get_follow_requests('follower1'))
        follow_requests = self.service.get_follow_requests('follower1')
        self.assertIn('follower1', follow_requests)

    def test_create_follow(self):
        """Test creating a follow relationship."""
        self.service.create_follow('user1', 'user3')
        followings = self.service.get_followings('user1')
        self.assertIn('user3', followings)

    def test_delete_follow(self):
        """Test deleting a follow relationship."""
        self.service.create_follow('user1', 'user4')
        self.service.delete_follow('user1', 'user4')
        followings = self.service.get_followings('user1')
        self.assertNotIn('user4', followings)

    def test_get_followers(self):
        """Test retrieving followers."""
        self.service.create_follow('user5', 'user2')
        followers = self.service.get_followers('user2')
        self.assertIn('user5', followers)

    def test_get_followings(self):
        """Test retrieving followings."""
        self.service.create_follow('user1', 'user6')
        followings = self.service.get_followings('user1')
        self.assertIn('user6', followings)

if __name__ == '__main__':
    unittest.main()
