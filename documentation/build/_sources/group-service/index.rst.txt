Group Service Documentation
============================

This documentation outlines the functionalities and methods provided by the GroupService class.

Initialization
--------------

Upon initialization, the GroupService class establishes connections to DynamoDB tables and sets up necessary configurations.

    ``GroupService()``
        Initializes the GroupService class.

    ``_get_dynamodb_resource()``
        Retrieves the DynamoDB resource based on the environment. It defaults to 'development' but switches to 'test' if specified.

    ``initialize_table(table_name, hash_key, sort_key=None, gsi=None)``
        Initializes a DynamoDB table with specified attributes.
        :param table_name: Name of the DynamoDB table.
        :param hash_key: Hash key attribute.
        :param sort_key: Sort key attribute (optional).
        :param gsi: Global Secondary Index details (optional).

Group Management
----------------

These methods facilitate group creation, retrieval, modification, and deletion.

    ``create_group(group_id, group_name, description, user_id)``
        Creates a new group.
        :param group_id: Unique identifier for the group.
        :param group_name: Name of the group.
        :param description: Description of the group.
        :param user_id: ID of the user creating the group.

    ``get_group(group_id)``
        Retrieves group details based on the group ID.
        :param group_id: Unique identifier for the group.

    ``edit_group_description(group_id, updated_description)``
        Modifies the description of a group.
        :param group_id: Unique identifier for the group.
        :param updated_description: New description for the group.

    ``add_user_to_group(user_id, group_id)``
        Adds a user to a group.
        :param user_id: ID of the user to be added.
        :param group_id: Unique identifier for the group.

    ``remove_user_from_group(user_id, group_id)``
        Removes a user from a group.
        :param user_id: ID of the user to be removed.
        :param group_id: Unique identifier for the group.

    ``get_group_members(group_id)``
        Retrieves members of a group.
        :param group_id: Unique identifier for the group.

Post Management
---------------

These methods facilitate post creation, retrieval, modification, and deletion within groups.

    ``create_post(group_id, content, posted_by)``
        Creates a new post within a group.
        :param group_id: Unique identifier for the group.
        :param content: Content of the post.
        :param posted_by: ID of the user posting the content.

    ``edit_post(group_id, post_id, updated_content)``
        Modifies the content of a post within a group.
        :param group_id: Unique identifier for the group.
        :param post_id: Unique identifier for the post.
        :param updated_content: New content for the post.

    ``delete_post(group_id, post_id)``
        Deletes a post within a group.
        :param group_id: Unique identifier for the group.
        :param post_id: Unique identifier for the post.

    ``get_posts_in_group(group_id)``
        Retrieves all posts within a group.
        :param group_id: Unique identifier for the group.
