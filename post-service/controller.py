import cherrypy
from services.post_service import PostService

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
            input_json = cherrypy.request.json
            post_id = input_json.get('post_id')
            title = input_json.get('title')
            content = input_json.get('content')
            author_id = input_json.get('author_id')
            timestamp = input_json.get('timestamp')
            video_url = input_json.get('video_url')

            self.post_service.create_post(post_id, title, content, author_id, timestamp, video_url)
            return {'status': 'success', 'message': 'Post creation successful.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_post(self, post_id):
        try:
            post = self.post_service.get_post(post_id)
            if post:
                return {'status': 'success', 'post': post}
            else:
                return {'status': 'error', 'message': 'Post not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8090})
    cherrypy.quickstart(PostController())
