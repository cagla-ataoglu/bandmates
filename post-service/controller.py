import cherrypy
import os
import json

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
    def create_post(self, content):
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

                input_json = cherrypy.request.json
                title = input_json.get('title')
                user_id = input_json.get('user_id')
                video_url = input_json.get('video_url')

                created_post = self.post_service.create_post(post_id, title, content, user_id, timestamp)

                return {'status': 'success', 'message': 'Post creation successful.', 'post': created_post}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        else:
            raise cherrypy.HTTPError(405, "Method Not Allowed")

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
