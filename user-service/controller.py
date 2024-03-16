import cherrypy
from services.cognito_service import CognitoService
from services.dynamodb_service import DynamoDBService

class UserService:

    def __init__(self):
        self.cognito_service = CognitoService()
        self.dynamodb_service = DynamoDBService()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to the User Service"}

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
            self.dynamodb_service.signup_user(username, email)
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
            user = self.dynamodb_service.get_user(username)
            return {
                'status': 'success',
                'tokens': tokens,
                'user': user
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
    cherrypy.quickstart(UserService())
