import cherrypy
from services.cognito_service import CognitoService

class AuthController:

    def __init__(self):
        self.cognito_service = CognitoService()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to the Auth Service"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def signup(self):
        try:
            input_json = cherrypy.request.json
            username = input_json.get('username')
            password = input_json.get('password')
            email = input_json.get('email')

            self.cognito_service.signup_user(username, password, email)
            return {'status': 'success', 'message': 'User registration successful.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def signin(self):
        input_json = cherrypy.request.json
        username = input_json.get('username')
        password = input_json.get('password')

        try:
            tokens = self.cognito_service.authenticate_user(username, password)
            return {
                'status': 'success',
                'tokens': tokens
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def validate(self, token):
        return self.cognito_service.validate_token(token)

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(AuthService())
