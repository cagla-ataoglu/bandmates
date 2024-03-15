import cherrypy

class UserService:
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to the User Service"}

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        # Endpoint to handle user registration
        input_json = cherrypy.request.json
        username = input_json.get('username')
        password = input_json.get('password')
        email = input_json.get('email')

        cognito_service = CognitoService()
        response = cognito_service.register_user(username, password, email)
        
        return response

if __name__ == '__main__':
    # Update the configuration to serve on all interfaces and port 8080
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(UserService())
