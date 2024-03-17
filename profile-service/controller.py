import cherrypy

class ProfileService:

    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to Profile Service"}
    
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(ProfileService())
