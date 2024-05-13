import boto3
from boto3.dynamodb.conditions import Key
import os

class GigNotFoundException(Exception):
    """Exception raised when a gig is not found."""
    pass

class GigAlreadyExistsException(Exception):
    """Exception raised when a gig already exists."""
    pass

class DynamoDBService:
    def __init__(self):
        """
            Initializes DynamoDBService with the necessary resources and table.
        """
        self.environment = os.getenv('ENV', 'development')
        self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566' if self.environment == 'development' else None)

        self.table_name = 'Gigs'

        try:
            self.dynamodb.Table(self.table_name).load()
            print(f"Table '{self.table_name}' already exists. Loading it.")
        except Exception as e:
            if 'ResourceNotFoundException' in str(e):
                table = self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {'AttributeName': 'GigId', 'KeyType': 'HASH'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'GigId', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
                table.meta.client.get_waiter('table_exists').wait(TableName=self.table_name)
                print("Gigs table created.")
            else:
                raise
        self.gigs_table = self.dynamodb.Table(self.table_name)

    def gig_exists(self, gig_id):
        """
            Checks if a given gig exists.

            Args:
                gig_id (str): The id of the gig.

            Returns:
                bool: True if the gig exists, False otherwise.
        """
        response = self.gigs_table.get_item(Key={'GigId': gig_id})
        return 'Item' in response

    def create_gig(self, gig_id, gig_name, date, band_username, venue, genre, looking_for, timestamp):
        """
            Creates a new gig entry in the DynamoDB table.

            Args:
                gig_id (str): The id of the gig.
                gig_name (str): The name of the gig.
                date (str): The date of the gig.
                band_username (str): The username of the band performing.
                venue (str): The venue of the gig.
                genre (str): The genre of the gig.
                looking_for (str): The type of participants the gig is looking for.
                timestamp (str): The time the gig is posted.

            Raises:
                GigAlreadyExistsException: If a gig with the same name and date already exists.
        """
        if self.gig_exists(gig_id):
            raise GigAlreadyExistsException(f"Gig with ID '{gig_id}' already exists.")
        else:
            item = {
                'GigId': gig_id,
                'GigName': gig_name,
                'GigDate': date,
                'BandUsername': band_username,
                'Venue': venue,
                'Genre': genre,
                'LookingFor': looking_for,
                'Timestamp': timestamp
            }
            self.gigs_table.put_item(Item=item)
            print("Gig created.", item)

    def get_gig(self, gig_id):
        """
            Retrieves information about a specific gig.

            Args:
                gig_id(str): The id of the gig.

            Returns:
                dict or None: Information about the gig if found, None otherwise.
        """
        response = self.gigs_table.get_item(Key={'GigId': gig_id})
        return response.get('Item')

    def scan_table(self):
        response = self.gigs_table.scan()
        return response['Items']

    def update_gig(self, gig_id, **kwargs):
        """
            Updates information about a gig.

            Args:
                gig_id (str): The id of the gig.
                kwargs: Additional attributes to update.

            Raises:
                GigNotFoundException: If the specified gig is not found.
        """
        if not self.gig_exists(gig_id):
            raise GigNotFoundException(f"Gig with ID '{gig_id}' not found.")

        update_expression = "SET " + ', '.join(f"#{k} = :{k}" for k in kwargs.keys())
        expression_attribute_values = {f":{k}": v for k, v in kwargs.items()}
        expression_attribute_names = {f"#{k}": k for k in kwargs.keys()}

        self.gigs_table.update_item(
            Key={'GigId': gig_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )

    def delete_gig(self, gig_id):
        """
            Deletes a gig entry from the DynamoDB table.

            Args:
                gig_id (str): The id of the gig.

            Returns:
                bool: True if the deletion was successful, False otherwise.
        """
        try:
            self.gigs_table.delete_item(Key={'GigId': gig_id})
            return True
        except Exception as e:
            print(f"Error deleting gig: {e}")
            return False
