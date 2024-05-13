Gig Service Module
=======================

This module provides functionalities for managing gigs stored in a DynamoDB table, including creating, updating, and deleting gigs. It also includes custom exceptions for handling specific errors related to gig operations.

Custom Exceptions
-----------------

.. autoclass:: dynamodb_service.GigNotFoundException
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: dynamodb_service.GigAlreadyExistsException
   :members:
   :undoc-members:
   :show-inheritance:

DynamoDB Service Class
----------------------

The ``DynamoDBService`` class encapsulates methods for interacting with the DynamoDB to manage gig-related data.

.. autoclass:: dynamodb_service.DynamoDBService
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members: