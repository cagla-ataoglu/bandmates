Profile Service Test
====================

Setup
-----

Environment Variables: AWS credentials and configuration are set up for testing (``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_DEFAULT_REGION``, ``ENV``).

Setup/Teardown:
- ``setUpClass(cls)``: Initializes mocks for DynamoDB and S3, sets up the DynamoDB table for profiles.
- ``tearDownClass(cls)``: Stops the mocked DynamoDB and S3 services.
- ``setUp(self)``: Initializes ProfileService for use in each test.

Test Functions:
- ``test_create_musician_profile(self)``: Verifies creating a musician profile and retrieving it.
- ``test_update_display_name(self)``: Checks functionality to update a musician's display name.
- ``test_add_remove_genre(self)``: Ensures genres can be added to and removed from a musician's profile.
- ``test_add_remove_instrument(self)``: Tests adding and removing instruments in a musician's profile.
