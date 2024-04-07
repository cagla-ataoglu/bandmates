import boto3

class GigNotFoundException(Exception):
    """Exception raised when a gig is not found."""
    pass

class GigAlreadyExistsException(Exception):
    """Exception raised when a gig already exists."""
    pass

class DynamoDBService:
    def __init__(self):
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

    # method to check if a given gig exists
    def gig_exists(self, gig_name, date):
        response = self.dynamodb.Table(self.table_name).query(
            KeyConditionExpression=Key('Date').eq(date) & Key('GigName').eq(gig_name)
        )
        return len(response['Items']) > 0

    # method to create a gig
    def create_gig(self, gig_name, date, band_name, venue, genre, looking_for):
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

    # method to read a gig
    def get_gig(self, gig_name, date):
        response = self.dynamodb.Table(self.table_name).get_item(Key={'Date': date, 'GigName': gig_name})
        
        if 'Item' in response:
            return response['Item']
        else:
            return None

    # method to read all the gigs
    def scan_table(self):
        response = self.dynamodb.Table(self.table_name).scan()
        return response['Items']

    # method to update a gig
    def update_gig(self, gig_name, date, **kwargs):
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

    # method to delete a gig
    def delete_gig(self, gig_name, date):
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

