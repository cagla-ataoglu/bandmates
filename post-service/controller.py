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
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create_post(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
            cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
            return ''
        elif cherrypy.request.method == 'POST':
            try:
                post_id = str(uuid.uuid4())
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                data = cherrypy.request.json
                content = data.get('content')
                user_id = data.get('user_id')

                created_post = self.post_service.create_post(post_id, content, user_id, timestamp)

                return {
                    'status': 'success',
                    'message': 'Post creation successful.',
                    'post_id': post_id  
                }
            except Exception as e:
                print("Error:", e)
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
