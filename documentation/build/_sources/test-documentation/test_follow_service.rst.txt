Test follow service documentation
==================================

Setup
-----

Environment Variables: Set up with mock AWS credentials to facilitate isolated testing (``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_SESSION_TOKEN``, ``AWS_DEFAULT_REGION``, ``ENV``).

Setup/Teardown
--------------

- ``setUpClass(cls)``: Initializes the mock environment for DynamoDB and creates an instance of FollowService.
- ``tearDownClass(cls)``: Stops the DynamoDB mock and resets any environment variables altered during setup.

Test Methods
------------

- ``test_create_follow()``: Verifies that creating a follow relationship between two users is successful and checks if the followed user is listed correctly.
- ``test_delete_follow()``: Tests the deletion of a follow relationship and ensures the user is no longer followed.
- ``test_get_followers()``: Tests retrieving the list of followers for a specific user to verify the correct followers are returned.
