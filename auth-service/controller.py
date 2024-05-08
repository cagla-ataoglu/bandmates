import cherrypy
from services.cognito_service import CognitoService


def cors_tool():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy.Tool('before_finalize', cors_tool, priority=60)

class AuthController:

    def __init__(self):
        self.cognito_service = CognitoService()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def index(self):
        return {"message": "Welcome to the Auth Service"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.cors()
    def signup(self):
        if cherrypy.request.method == 'POST':
            try:
                input_json = cherrypy.request.json
                username = input_json.get('username')
                password = input_json.get('password')
                email = input_json.get('email')

                self.cognito_service.signup_user(username, password, email)
                return {'status': 'success', 'message': 'User registration successful.'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.cors()
    def signin(self):
        if cherrypy.request.method == 'POST':
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
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def validate(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            token = input_json.get('token')
            return self.cognito_service.validate_token(token)
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.cors()
    def change_password(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            access_token = input_json.get('access_token')
            old_password = input_json.get('old_password')
            new_password = input_json.get('new_password')

            result = self.cognito_service.change_password(access_token, old_password, new_password)
            return result
        return ''
# Test c
if __name__ == '__main__':
    config = {
        '/': {
            'tools.sessions.on': True,
            'tools.cors.on': True
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(AuthController(), '/', config)
