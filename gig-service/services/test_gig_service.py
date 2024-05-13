import unittest
from unittest.mock import patch
from moto import mock_dynamodb2
import boto3
import os
from dynamodb_service import DynamoDBService, GigNotFoundException, GigAlreadyExistsException
from boto3.dynamodb.conditions import Key
import uuid
import time

# Mock environment variables
os.environ["AWS_ACCESS_KEY_ID"] = "fake_id"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_secret"
os.environ["AWS_SESSION_TOKEN"] = "fake_session_token"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["ENV"] = "test"

class TestDynamoDBService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the DynamoDB table for testing."""
        cls.mock = mock_dynamodb2()
        cls.mock.start()
        cls.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        cls.table = cls.dynamodb.create_table(
            TableName='Gigs',
            KeySchema=[
                {'AttributeName': 'GigId', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'GigId', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        cls.table.wait_until_exists()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment."""
        cls.table.delete()
        cls.mock.stop()

    def setUp(self):
        """Instantiate the DynamoDBService before each test."""
        self.service = DynamoDBService()

    def test_create_gig(self):
        """Test creating a gig."""
        gig_id = str(uuid.uuid4())
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.service.create_gig(gig_id, "Rock Night", "2023-09-15", "The Wild Ones", "RockArena", "Rock", "Guitarist", timestamp)
        gig = self.service.get_gig(gig_id)
        self.assertIsNotNone(gig)
        self.assertEqual(gig['BandUsername'], "The Wild Ones")

    def test_create_gig_already_exists(self):
        """Test creating a gig that already exists should raise an exception."""
        gig_id = str(uuid.uuid4())
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.service.create_gig(gig_id, "Jazz Evening", "2023-09-16", "Smooth Jazz Band", "JazzBar", "Jazz", "Drummer", timestamp)
        with self.assertRaises(GigAlreadyExistsException):
            self.service.create_gig(gig_id, "Jazz Evening", "2023-09-16", "Smooth Jazz Band", "JazzBar", "Jazz", "Drummer", timestamp)

    def test_get_gig_not_found(self):
        """Test getting a non-existing gig."""
        gig = self.service.get_gig("Non-existent Gig")
        self.assertIsNone(gig)

    def test_update_gig(self):
        """Test updating an existing gig."""
        gig_id = str(uuid.uuid4())
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.service.create_gig(gig_id, "Pop Night", "2023-09-18", "Pop Stars", "PopVenue", "Pop", "Singer", timestamp)
        self.service.update_gig(gig_id, BandUsername="New Pop Stars")
        gig = self.service.get_gig(gig_id)
        self.assertEqual(gig['BandUsername'], "New Pop Stars")

    def test_update_gig_not_found(self):
        """Test updating a non-existing gig should raise an exception."""
        gig_id = str(uuid.uuid4())
        with self.assertRaises(GigNotFoundException):
            self.service.update_gig(gig_id, Venue="New Venue")

    def test_delete_gig(self):
        """Test deleting an existing gig."""
        gig_id = str(uuid.uuid4())
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.service.create_gig(gig_id, "Folk Night", "2023-09-20", "Folk Band", "FolkPub", "Folk", "Violinist", timestamp)
        deleted = self.service.delete_gig(gig_id)
        self.assertTrue(deleted)
        gig = self.service.get_gig(gig_id)
        self.assertIsNone(gig)

if __name__ == '__main__':
    unittest.main()
