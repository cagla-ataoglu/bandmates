import cherrypy
import os
import json
import requests
from services.post_service import PostService
import uuid
import time

class PostController:
    def __init__(self):
        self.post_service = PostService()

    @cherrypy.expose
    def index(self):
        return {"message": "Welcome to the Post Service"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def create_post(self, user_id=None, content=None):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
            cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
            return ''
        elif cherrypy.request.method == 'POST':
            if not content:
                return {"error": "No file uploaded"}

            try:
                post_id = str(uuid.uuid4())
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                created_post = self.post_service.create_post(post_id, content, user_id, timestamp)

                return {'status': 'success', 'message': 'Post creation successful.', 'post': created_post}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        else:
            raise cherrypy.HTTPError(405, "Method Not Allowed")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_post_by_id(self, post_id=None):
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

    @cherrypy.expose
    def download_post_content(self, post_id=None):
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

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def display_posts(self):
        try:
            # Fetch posts from the database
            posts = self.post_service.get_all_posts()
            return {'status': 'success', 'posts': posts}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def clear_all_posts(self):
        try:
            self.post_service.clear_all_posts()
            return {'status': 'success', 'message': 'All posts cleared successfully.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8090})
    cherrypy.quickstart(PostController())
