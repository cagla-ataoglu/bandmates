import cherrypy
import os
import json
import requests
from services.post_service import PostService
import uuid
import time

def cors_tool():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy.Tool('before_finalize', cors_tool, priority=60)

class PostController:
    def __init__(self):
        self.environment = os.getenv('ENV', 'development')
        self.auth_endpoint_url = 'http://auth-service-env.eba-sawkmqsi.us-east-1.elasticbeanstalk.com' if self.environment == 'production' else 'http://auth-service:8080'
        self.post_service = PostService()

    @cherrypy.expose
    def index(self):
        return {"message": "Welcome to the Post Service"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def create_post(self, content=None, description=''):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
            cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
            return ''
        elif cherrypy.request.method == 'POST':
            auth_header = cherrypy.request.headers.get('Authorization')
            if not auth_header:
                return {'status': 'error', 'message': 'Authorization header missing'}

            token = auth_header.split(" ")[1]

            payload = {'token': token}
            response = requests.post('http://auth-service:8080/validate', json=payload)
            response = response.json()
            if response['status'] != 'success':
                return {'status': 'error', 'message': 'Token validation failed'}

            user_info = response['user_info']
            username = user_info['username']

            if not content:
                return {"error": "No file uploaded"}

            try:
                post_id = str(uuid.uuid4())
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                created_post = self.post_service.create_post(post_id, description, content, username, timestamp)

                return {'status': 'success', 'message': 'Post creation successful.', 'post': created_post}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_post_by_id(self, post_id=None):
        if cherrypy.request.method == 'POST':
            if post_id is None:
                return {'status': 'error', 'message': 'No post_id provided'}

            try:
                post = self.post_service.get_post_by_id(post_id)
                if post:
                    return {'status': 'success', 'post': post}
                else:
                    return {'status': 'error', 'message': 'Post not found'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.cors()
    def download_post_content(self, post_id=None):
        if cherrypy.request.method == 'POST':
            if post_id is None:
                return "No post_id provided"

            try:
                post = self.post_service.get_post_by_id(post_id)
                content_url = post['url']
                content_response = requests.get(content_url)

                cherrypy.response.headers['Content-Type'] = 'application/octet-stream'
                cherrypy.response.headers['Content-Disposition'] = f'attachment; filename="{post_id}.png"'

                return content_response.content
            except Exception as e:
                return str(e)
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def display_posts(self):
        if cherrypy.request.method == 'POST':
            try:
                # Fetch posts from the database
                posts = self.post_service.get_all_posts()
                return {'status': 'success', 'posts': posts}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def clear_all_posts(self):
        if cherrypy.request.method == 'POST':
            try:
                self.post_service.clear_all_posts()
                return {'status': 'success', 'message': 'All posts cleared successfully.'}
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
    cherrypy.config.update({'server.socket_port': 8090})
    cherrypy.quickstart(PostController(), '/', config)
