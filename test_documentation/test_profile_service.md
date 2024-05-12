# Test profile service documentation
### Setup

**Environment Variables**: AWS credentials and configuration are set up for testing (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `ENV`).

### Setup/Teardown:

`setUpClass(cls)`: Initializes mocks for DynamoDB and S3, sets up the DynamoDB table for profiles.  
`tearDownClass(cls)`: Stops the mocked DynamoDB and S3 services.  
`setUp(self)`: Initializes ProfileService for use in each test.  

### Test Functions:

`test_band_create_profile(self)`: Verifies creating a band profile and retrieving it.
`test_band_update_location(self)`: Ensures location of a profile can be updated.
`test_band_add_remove_member(self)`: Tests adding and removing members to and from a band.
`test_band_add_remove_genre(self)`: Tests adding and removing a genre to and from a band.
`test_band_update_looking_for_members(self)`: Verifies "looking for members" of a band profile can be toggled.
`test_musician_create_profile(self)`: Verifies creating a musician profile and retrieving it.  
`test_musician_update_display_name(self)`: Checks functionality to update a musician's display name.  
`test_add_remove_genre(self)`: Ensures genres can be added to and removed from a musician's profile.  
`test_add_remove_instrument(self)`: Tests adding and removing instruments in a musician's profile.
`test_musician_update_looking_for_gigs(self)`: Verifies "looking for gigs" of a musician profile can be toggled.