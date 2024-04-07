import cherrypy
from services.dynamodb_service import DynamoDBService

class ProfileService:

    def __init__(self):
        self.dynamodb_service = DynamoDBService()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {'message': 'Welcome to Profile Service'}
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create_musician_profile(self):
        data = cherrypy.request.json
        username = data.get('username')
        if not username:
            raise cherrypy.HTTPError(400, 'Username is required.')
        
        display_name = data.get('display_name')
        instruments = data.get('instruments')
        genres = data.get('genres')
        location = data.get('location')

        self.dynamodb_service.createMusicianProfile(username, display_name, instruments, genres, location)
        return {'message': f'Musician profile created for {username}.'}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create_band_profile(self):
        data = cherrypy.request.json
        username = data.get('username')
        if not username:
            raise cherrypy.HTTPError(400, 'Username is required.')
        
        display_name = data.get('display_name')
        members = data.get('members')
        genres = data.get('genres')
        location = data.get('location')

        self.dynamodb_service.createBandProfile(username, display_name, members, genres, location)
        return {'message': f'Band profile created for {username}.'}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_profile(self, username):
        profile = self.dynamodb_service.getProfile(username)
        if profile:
            return profile
        else:
            raise cherrypy.HTTPError(404, f'No profile found for {username}.')
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update_display_name(self):
        data = cherrypy.request.json
        username = data.get('username')
        new_display_name = data.get('display_name')
        if not username or not new_display_name:
            raise cherrypy.HTTPError(400, 'Username and display name required.')
        
        try:
            self.dynamodb_service.updateDisplayName(username, new_display_name)
            return {'message': f'Display name updated for {username} to {new_display_name}.'}
        except Exception as e:
            raise cherrypy.HTTPError(500, f'Error updating display name for {username}: {e}')
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update_location(self):
        data = cherrypy.request.json
        username = data.get('username')
        new_location = data.get('location')
        if not username or not new_location:
            raise cherrypy.HTTPError(400, 'Username and location required.')
        
        try:
            self.dynamodb_service.updateLocation(username, new_location)
            return {'message': f'Location updated for {username} to {new_location}.'}
        except Exception as e:
            raise cherrypy.HTTPError(500, f'Error updating location for {username}: {e}')

    
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(ProfileService())
