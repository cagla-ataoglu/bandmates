import os
import unittest
from unittest.mock import patch
from moto import mock_dynamodb2, mock_s3
import boto3
from dynamodb_service import DynamoDBService, sets_to_lists

# Set up mocked AWS Credentials
os.environ["AWS_ACCESS_KEY_ID"] = "fake_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_secret"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ['ENV'] = 'test'

class TestDynamoDBService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_dynamodb = mock_dynamodb2()
        cls.mock_dynamodb.start()
        cls.mock_s3 = mock_s3()
        cls.mock_s3.start()

        # Continue with your DynamoDB setup
        cls.dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        cls.table = cls.dynamodb.create_table(
            TableName='Profiles',
            KeySchema=[{'AttributeName': 'username', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'username', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        cls.table.wait_until_exists()

    @classmethod
    def tearDownClass(cls):
        cls.mock_dynamodb.stop()
        cls.mock_s3.stop()

    def setUp(self):
        """Instantiate the service before each test."""
        self.service = DynamoDBService()

    def test_create_musician_profile(self):
        self.service.createMusicianProfile("johndoe", "John Doe", "New York")
        response = self.service.getProfile("johndoe")
        self.assertEqual(response['display_name'], "John Doe")

    def test_update_display_name(self):
        self.service.createMusicianProfile("janedoe", "Jane Doe", "Los Angeles")
        self.service.updateDisplayName("janedoe", "Jane D.")
        response = self.service.getProfile("janedoe")
        self.assertEqual(response['display_name'], "Jane D.")

    def test_add_remove_genre(self):
        username = "johndoe"
        self.service.createMusicianProfile(username, "John Doe", "New York")
        self.service.addGenre(username, "Jazz")
        profile = self.service.getProfile(username)
        self.assertIn("Jazz", sets_to_lists(profile['genres']))
        
        self.service.removeGenre(username, "Jazz")
        profile = self.service.getProfile(username)
        self.assertNotIn("Jazz", sets_to_lists(profile.get('genres', [])))

    def test_add_remove_instrument(self):
        username = "janedoe"
        self.service.createMusicianProfile(username, "Jane Doe", "Los Angeles")
        self.service.addInstrument(username, "Guitar")
        profile = self.service.getProfile(username)
        self.assertIn("Guitar", sets_to_lists(profile['instruments']))

        self.service.removeInstrument(username, "Guitar")
        profile = self.service.getProfile(username)
        self.assertNotIn("Guitar", sets_to_lists(profile.get('instruments', [])))

if __name__ == '__main__':
    unittest.main()
