Gig Service Test
================

Setup
-----

Environment Variables: Mock AWS credentials and settings are configured to facilitate testing without real AWS services (``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_SESSION_TOKEN``, ``AWS_DEFAULT_REGION``, ``ENV``).

Setup/Teardown
--------------

- ``setUpClass(cls)``: Initializes the mock environment and sets up the DynamoDB table used to store gig data.
- ``tearDownClass(cls)``: Tears down the mock environment and deletes the DynamoDB table.
- ``setUp(self)``: Creates an instance of DynamoDBService for use in each test method.

Test Methods
------------

- ``test_create_gig()``: Tests the creation of a gig and verifies the entry's correct storage and retrieval.
- ``test_create_gig_already_exists()``: Ensures that attempting to create a duplicate gig entry raises a GigAlreadyExistsException.
- ``test_get_gig_not_found()``: Attempts to retrieve a non-existent gig to ensure that the appropriate response (none) is returned.
- ``test_update_gig()``: Tests updating the details of an existing gig and checks if the updates are accurately reflected.
- ``test_update_gig_not_found()``: Confirms that trying to update a non-existent gig raises a GigNotFoundException.
- ``test_delete_gig()``: Validates the functionality to delete a gig and ensure it no longer exists in the database.
