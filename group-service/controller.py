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

            input_json = cherrypy.request.json
            #group_id = input_json.get('group_id')
            group_name = input_json.get('group_name')
            description = input_json.get('description')
            user_id = input_json.get('user_id')

            print("Creating group with the following attributes:")
            print(f"Group ID: {group_id}")
            print(f"Group Name: {group_name}")
            print(f"Description: {description}")
            print(f"Creator User ID: {user_id}")

            created_group = self.group_service.create_group(group_id, group_name, description, user_id)


            return {'status': 'success', 'message': 'Group creation successful.', 'group': created_group}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def edit_group_description(self):
        try:
            input_json = cherrypy.request.json
            group_id = input_json.get('group_id')
            updated_description = input_json.get('description')

            self.group_service.edit_group_description(group_id, updated_description)
            return {'status': 'success', 'message': 'Group edit successful.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_group(self, group_id):
        try:
            group = self.group_service.get_group(group_id)
            if group:
                return {'status': 'success', 'group': group}
            else:
                return {'status': 'error', 'message': 'Group not found'}
        except Exception as e:
                return {'status': 'error', 'message': str(e)}

    #TODO: Add join group
    #TODO: Add leave group
    #TODO: Add get group members
    #TODO: (Possibly) Add post service
        
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8088})
    cherrypy.quickstart(GroupController())
