DynamoDB Service
================

.. code:: python

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
        """
        DynamoDBService is a class to manage interactions with a DynamoDB table for storing gigs.

        Attributes:
            environment (str): The environment in which the service is running. Default is 'development'.
            dynamodb (boto3.resource): The DynamoDB resource.
            table_name (str): The name of the DynamoDB table for gigs.
            gigs_table (boto3.resource.Table): The DynamoDB table for gigs.
        """

        def __init__(self):
            """
            Initializes DynamoDBService with the necessary resources and table.
            """
            self.environment = os.getenv('ENV', 'development')
            if self.environment == 'test':
                self.dynamodb = boto3.resource('dynamodb')
            else:
                self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
            self.table_name = 'Gigs'
            # Ensure Gigs table exists
            try:
                self.dynamodb.Table(self.table_name).load()
                print(f"Table '{self.table_name}' already exists. Loading it.")
            except Exception as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    table = self.dynamodb.create_table(
                        TableName='Gigs',
                        KeySchema=[{'AttributeName': 'Date', 'KeyType': 'HASH'}, {'AttributeName': 'GigName', 'KeyType': 'RANGE'}],
                        AttributeDefinitions=[{'AttributeName': 'Date', 'AttributeType': 'S'}, {'AttributeName': 'GigName', 'AttributeType': 'S'}],
                        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    )
                    table.meta.client.get_waiter('table_exists').wait(TableName='Gigs')
                    print("Gigs table created.")
                else:
                    raise
            self.gigs_table = self.dynamodb.Table('Gigs')

        def gig_exists(self, gig_name, date):
            """
            Checks if a given gig exists.

            Args:
                gig_name (str): The name of the gig.
                date (str): The date of the gig.

            Returns:
                bool: True if the gig exists, False otherwise.
            """
            response = self.dynamodb.Table(self.table_name).query(
                KeyConditionExpression=Key('Date').eq(date) & Key('GigName').eq(gig_name)
            )
            return len(response['Items']) > 0

        def create_gig(self, gig_name, date, band_name, venue, genre, looking_for):
            """
            Creates a new gig entry in the DynamoDB table.

            Args:
                gig_name (str): The name of the gig.
                date (str): The date of the gig.
                band_name (str): The name of the band performing.
                venue (str): The venue of the gig.
                genre (str): The genre of the gig.
                looking_for (str): The type of participants the gig is looking for.

            Raises:
                GigAlreadyExistsException: If a gig with the same name and date already exists.
            """
            if self.gig_exists(gig_name, date):
                raise GigAlreadyExistsException(f"Gig '{gig_name}' on {date} already exists.")
            else: 
                self.gigs_table.put_item(
                    Item={
                        'GigName': gig_name,
                        'Date': date,
                        'BandName': band_name,
                        'Venue': venue,
                        'Genre': genre,
                        'LookingFor': looking_for
                    }
                )
                print("Gig created.")

        def get_gig(self, gig_name, date):
            """
            Retrieves information about a specific gig.

            Args:
                gig_name (str): The name of the gig.
                date (str): The date of the gig.

            Returns:
                dict or None: Information about the gig if found, None otherwise.
            """
            response = self.dynamodb.Table(self.table_name).get_item(Key={'Date': date, 'GigName': gig_name})
            
            if 'Item' in response:
                return response['Item']
            else:
                return None

        def scan_table(self):
            """
            Scans the DynamoDB table and retrieves all gig entries.

            Returns:
                list: A list of dictionaries representing gig entries.
            """
            response = self.dynamodb.Table(self.table_name).scan()
            return response['Items']

        def update_gig(self, gig_name, date, **kwargs):
            """
            Updates information about a gig.

            Args:
                gig_name (str): The name of the gig.
                date (str): The date of the gig.
                **kwargs: Additional attributes to update.

            Raises:
                GigNotFoundException: If the specified gig is not found.
            """
            # check if the gig exists
            if not self.gig_exists(gig_name, date):
                raise GigNotFoundException(f"Gig '{gig_name}' on {date} not found.")

            # Build the update expression
            update_expression = "SET "
            expression_attribute_values = {}
            expression_attribute_names = {}

            for key, value in kwargs.items():
                update_expression += f"#{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
                expression_attribute_names[f"#{key}"] = key

            # Remove the trailing comma and space from the update expression
            update_expression = update_expression[:-2]

            # Update the gig item in the DynamoDB table
            self.dynamodb.Table(self.table_name).update_item(
                Key={
                    'Date': date,
                    'GigName': gig_name
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names
            )

        def delete_gig(self, gig_name, date):
            """
            Deletes a gig entry from the DynamoDB table.

            Args:
                gig_name (str): The name of the gig.
                date (str): The date of the gig.

            Returns:
                bool: True if the deletion was successful, False otherwise.
            """
            try:
                self.dynamodb.Table(self.table_name).delete_item(
                    Key={
                        'GigName': gig_name,
                        'Date': date
                    }
                )
                return True
            except Exception as e:
                print(f"Error deleting gig: {e}")
                return False
