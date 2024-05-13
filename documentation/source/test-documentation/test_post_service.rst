Test post service documentation
===============================

Setup
-----

Environment Variables: Key AWS credentials and configuration for test environment are mocked (``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_SESSION_TOKEN``, ``AWS_DEFAULT_REGION``, and ``ENV`` set to "test").

Tests in TestPostService
------------------------

Setup/Teardown:
- ``setUpClass(cls)``: Initializes and starts mocks for DynamoDB and S3, creates an instance of PostService.
- ``tearDownClass(cls)``: Stops the mocked AWS services.
- ``setUp(self)``: Prepares a mock file-like object mimicking Flask's FileStorage.

Test Functions:
- ``test_create_post(self)``: Validates post creation with necessary attributes and verifies the response.
- ``test_get_post_by_id(self)``: Ensures a post can be retrieved by its ID after creation.
- ``test_clear_all_posts(self)``: Tests the removal of all posts, verifying that no posts remain afterwards.
- ``test_edit_post_description(self)``: Confirms that a post's description can be updated and retrieved correctly.
- ``test_delete_post(self)``: Checks deletion functionality by ensuring a post cannot be retrieved after deletion.
