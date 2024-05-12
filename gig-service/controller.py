import cherrypy
from services.dynamodb_service import DynamoDBService
import uuid
import time

def cors_tool():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy.Tool('before_finalize', cors_tool, priority=60)

class GigService:

    def __init__(self):
        self.dynamodb_service = DynamoDBService()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"message": "Welcome to the Gig Service"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.cors()
    def post_gig(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            gig_id = str(uuid.uuid4())
            gig_name = input_json.get('gig_name')
            date = input_json.get('date')
            band_username = input_json.get('band_username')
            venue = input_json.get('venue')
            genre = input_json.get('genre')
            looking_for = input_json.get('looking_for')
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            if not gig_id or not band_username:
                raise cherrypy.HTTPError(400, 'Gig ID and band username are required.')

            try:
                self.dynamodb_service.create_gig(gig_id, gig_name, date, band_username, venue, genre, looking_for, timestamp)
                return {'status': 'success', 'message': 'Gig creation successful.'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_gig_postings(self):
        if cherrypy.request.method == 'POST':
            try:
                gig_postings = self.dynamodb_service.scan_table()
                return {'status': 'success', 'posts': gig_postings}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_gig(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            gig_id = input_json.get('gig_id')

            if not gig_id:
                raise cherrypy.HTTPError(400, 'Gig ID is required.')

            try:
                gig = self.dynamodb_service.get_gig(gig_id)
                if gig:
                    return {'status': 'success', 'gig': gig}
                else:
                    return {'status': 'error', 'message': 'Gig not found'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def update_gig(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            gig_id = input_json.get('gig_id')
            update_data = input_json

            if not gig_id:
                raise cherrypy.HTTPError(400, 'Gig ID is required.')

            try:
                self.dynamodb_service.update_gig(gig_id, **update_data)
                return {'status': 'success', 'message': 'Gig updated successfully'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def delete_gig(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            gig_id = input_json.get('gig_id')

            if not gig_id:
                raise cherrypy.HTTPError(400, 'Gig ID is required.')

            try:
                success = self.dynamodb_service.delete_gig(gig_id)
                if success:
                    return {'status': 'success', 'message': 'Gig deleted successfully'}
                else:
                    return {'status': 'error', 'message': 'Failed to delete gig'}
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
    cherrypy.config.update({'server.socket_port': 8082})
    cherrypy.quickstart(GigService(), '/', config)
