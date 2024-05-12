Profile Service Documentation
=============================

This documentation outlines the functionalities and methods provided by the ProfileService class.

Initialization
--------------

Upon initialization, the ProfileService class establishes connections to DynamoDB tables and S3 buckets based on the environment.

    ``ProfileService()``
        Initializes the ProfileService class.

        - If the environment is set to 'production':
            - Connects to DynamoDB and S3 in the AWS production environment.
            - Uses the base URL for S3 bucket access.
        - If the environment is set to 'test':
            - Connects to DynamoDB and S3 in the AWS test environment.
        - Otherwise:
            - Connects to DynamoDB and S3 in the local environment using LocalStack.
            - Uses the base URL for S3 bucket access in the local environment.

Profile Management
-------------------

These methods facilitate profile creation, retrieval, modification, and deletion.

    ``createMusicianProfile(username, display_name, location)``
        Creates a musician profile.
        :param username: Username of the musician.
        :param display_name: Display name of the musician.
        :param location: Location of the musician.

    ``createBandProfile(username, display_name, location)``
        Creates a band profile.
        :param username: Username of the band.
        :param display_name: Display name of the band.
        :param location: Location of the band.

    ``getProfile(username)``
        Retrieves profile details based on the username.
        :param username: Username of the profile.

    ``updateDisplayName(username, new_display_name)``
        Updates the display name of a profile.
        :param username: Username of the profile.
        :param new_display_name: New display name for the profile.

    ``updateLocation(username, new_location)``
        Updates the location of a profile.
        :param username: Username of the profile.
        :param new_location: New location for the profile.

    ``addGenre(username, genre)``
        Adds a genre to a musician's profile.
        :param username: Username of the musician.
        :param genre: Genre to be added.

    ``removeGenre(username, genre)``
        Removes a genre from a musician's profile.
        :param username: Username of the musician.
        :param genre: Genre to be removed.

    ``addInstrument(username, instrument)``
        Adds an instrument to a musician's profile.
        :param username: Username of the musician.
        :param instrument: Instrument to be added.

    ``removeInstrument(username, instrument)``
        Removes an instrument from a musician's profile.
        :param username: Username of the musician.
        :param instrument: Instrument to be removed.

    ``addMember(username, member)``
        Adds a member to a band's profile.
        :param username: Username of the band.
        :param member: Member to be added.

    ``removeMember(username, member)``
        Removes a member from a band's profile.
        :param username: Username of the band.
        :param member: Member to be removed.

    ``updateLookingForGigs(username, state)``
        Updates the "looking for gigs" status for a musician.
        :param username: Username of the musician.
        :param state: New status ("true" or "false").

    ``updateLookingForMembers(username, state)``
        Updates the "looking for members" status for a band.
        :param username: Username of the band.
        :param state: New status ("true" or "false").

    ``updateProfilePicture(username, picture)``
        Updates the profile picture for a profile.
        :param username: Username of the profile.
        :param picture: New profile picture.

    ``searchProfilesByUsernamePrefix(username_prefix, limit=7)``
        Searches for profiles based on username prefix.
        :param username_prefix: Prefix of the username to search for.
        :param limit: Maximum number of profiles to return (default: 7).
