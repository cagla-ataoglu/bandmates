import cherrypy
from services.post_service import PostService
import uuid
import time

class PostController:
    def __init__(self):
        self.post_service = PostService()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to the Post Service"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def create_post(self):
        try:

            post_id = str(uuid.uuid4())
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            input_json = cherrypy.request.json
            title = input_json.get('title')
            content = input_json.get('content')
            user_id = input_json.get('user_id')
            video_url = input_json.get('video_url')
            
            created_post = self.post_service.create_post(post_id, title, content, user_id, timestamp, video_url)

            #print("Created post:", created_post)

            return {'status': 'success', 'message': 'Post creation successful.', 'post': created_post}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # @cherrypy.expose
    # @cherrypy.tools.json_out()
    # def get_post(self, post_id):
    #     try:
    #         post = self.post_service.get_post(post_id)
    #         if post:
    #             return {'status': 'success', 'post': post}
    #         else:
    #             return {'status': 'error', 'message': 'Post not found'}
    #     except Exception as e:
    #         return {'status': 'error', 'message': str(e)}
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def edit_post(self):
        try:
            input_json = cherrypy.request.json
            post_id = input_json.get('post_id')
            updated_content = input_json.get('content')

            self.post_service.edit_post(post_id, updated_content)
            return {'status': 'success', 'message': 'Post edit successful.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8090})
    cherrypy.quickstart(PostController())
