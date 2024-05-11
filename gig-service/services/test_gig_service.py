import unittest
from unittest.mock import patch
from moto import mock_dynamodb2
import boto3
import os
from dynamodb_service import DynamoDBService, GigNotFoundException, GigAlreadyExistsException
from boto3.dynamodb.conditions import Key

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
                {'AttributeName': 'Date', 'KeyType': 'HASH'},
                {'AttributeName': 'GigName', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'Date', 'AttributeType': 'S'},
                {'AttributeName': 'GigName', 'AttributeType': 'S'}
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
        self.service.create_gig("Rock Night", "2023-09-15", "The Wild Ones", "RockArena", "Rock", "Guitarist")
        gig = self.service.get_gig("Rock Night", "2023-09-15")
        self.assertIsNotNone(gig)
        self.assertEqual(gig['BandName'], "The Wild Ones")

    def test_create_gig_already_exists(self):
        """Test creating a gig that already exists should raise an exception."""
        self.service.create_gig("Jazz Evening", "2023-09-16", "Smooth Jazz Band", "JazzBar", "Jazz", "Drummer")
        with self.assertRaises(GigAlreadyExistsException):
            self.service.create_gig("Jazz Evening", "2023-09-16", "Smooth Jazz Band", "JazzBar", "Jazz", "Drummer")

    def test_get_gig_not_found(self):
        """Test getting a non-existing gig."""
        gig = self.service.get_gig("Non-existent Gig", "2023-09-17")
        self.assertIsNone(gig)

    def test_update_gig(self):
        """Test updating an existing gig."""
        self.service.create_gig("Pop Night", "2023-09-18", "Pop Stars", "PopVenue", "Pop", "Singer")
        self.service.update_gig("Pop Night", "2023-09-18", BandName="New Pop Stars")
        gig = self.service.get_gig("Pop Night", "2023-09-18")
        self.assertEqual(gig['BandName'], "New Pop Stars")

    def test_update_gig_not_found(self):
        """Test updating a non-existing gig should raise an exception."""
        with self.assertRaises(GigNotFoundException):
            self.service.update_gig("Non-existent Gig", "2023-09-19", Venue="New Venue")

    def test_delete_gig(self):
        """Test deleting an existing gig."""
        self.service.create_gig("Folk Night", "2023-09-20", "Folk Band", "FolkPub", "Folk", "Violinist")
        deleted = self.service.delete_gig("Folk Night", "2023-09-20")
        self.assertTrue(deleted)
        gig = self.service.get_gig("Folk Night", "2023-09-20")
        self.assertIsNone(gig)

if __name__ == '__main__':
    unittest.main()
