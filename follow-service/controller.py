import cherrypy
from services.follow_service import FollowService


def cors_tool():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy.Tool('before_finalize', cors_tool, priority=60)

class FollowController:

    def __init__(self):
        self.follow_service = FollowService()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def index(self):
        return {"message": "Welcome to the Follow Service"}

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

    
if __name__ == '__main__':
    config = {
        '/': {
            'tools.sessions.on': True,
            'tools.cors.on': True 
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8083})
    cherrypy.quickstart(AuthController(), '/', config)
