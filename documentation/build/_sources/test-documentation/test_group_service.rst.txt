Test group service documentation
================================

Setup
-----

Environment Variables: AWS credentials and environment settings are mocked to facilitate testing of AWS services (``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_SECURITY_TOKEN``, ``AWS_SESSION_TOKEN``, ``AWS_DEFAULT_REGION``, ``ENV``).

Test Functions
--------------

- ``set_up()``: Initializes DynamoDB mock environment, creates necessary tables (Groups, UsersGroups, GroupPosts), and returns an instance of GroupService.
- ``test_create_group()``: Tests the creation of a group and validates that the returned group details match the expected values.
- ``test_get_group()``: Ensures that a created group can be retrieved and that its details are correct.
- ``test_edit_group_description()``: Confirms the ability to update a group's description and checks that the update is reflected.
- ``test_add_user_to_group()``: Verifies that a user can be added to a group and appears in the group members list.
- ``test_remove_user_from_group()``: Tests removing a user from a group and ensures the user is no longer listed as a group member.
- ``test_create_post()``: Checks the functionality of creating a post within a group and validates the presence and content of the post.
