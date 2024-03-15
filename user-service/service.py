import cherrypy

class UserService:
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to the User Service"}

if __name__ == '__main__':
    # Update the configuration to serve on all interfaces and port 8080
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(UserService())
