import cherrypy
from services.group_service import GroupService
import uuid
import time

class GroupController:
    def __init__(self):
        self.group_service = GroupService()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to the Group Service"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def create_group(self):
        try:

            group_id = str(uuid.uuid4())
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            input_json = cherrypy.request.json
            title = input_json.get('title')
            content = input_json.get('content')
            user_id = input_json.get('user_id')
            
            created_group = self.group_service.create_group(group_id, title, content, user_id, timestamp)


            return {'status': 'success', 'message': 'Group creation successful.', 'group': created_group}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def edit_group(self):
        try:
            input_json = cherrypy.request.json
            group_id = input_json.get('group_id')
            updated_content = input_json.get('content')

            self.group_service.edit_group(group_id, updated_content)
            return {'status': 'success', 'message': 'Group edit successful.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8088})
    cherrypy.quickstart(GroupController())
