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
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def send_follow_request(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            follower = input_json.get('follower')
            following = input_json.get('following')
            self.follow_service.send_follow_request(follower, following)

            return {'status': 'success'}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def follow(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            follower = input_json.get('follower')
            following = input_json.get('following')
            self.follow_service.create_follow(follower, following)

            return {'status': 'success'}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def unfollow(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            follower = input_json.get('follower')
            following = input_json.get('following')
            self.follow_service.delete_follow(follower, following)

            return {'status': 'success'}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_followings(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            username = input_json.get('username')
            followings = self.follow_service.get_followings(username)

            return {'status': 'success', 'followings': followings}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_followers(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            username = input_json.get('username')
            followers = self.follow_service.get_followers(username)

            return {'status': 'success', 'followers': followers}
        return ''

# Minor change    
if __name__ == '__main__':
    config = {
        '/': {
            'tools.sessions.on': True,
            'tools.cors.on': True 
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8083})
    cherrypy.quickstart(FollowController(), '/', config)
