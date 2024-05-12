import cherrypy
from services.dynamodb_service import DynamoDBService

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
            try:
                input_json = cherrypy.request.json
                gig_name = input_json.get('gig_name')
                date = input_json.get('date')

                if not gig_name or not date:
                    raise cherrypy.HTTPError(400, 'Gig name and date are required.')

                band_name = input_json.get('band_name')
                venue = input_json.get('venue')
                genre = input_json.get('genre')
                looking_for = input_json.get('looking_for')

                self.dynamodb_service.create_gig(gig_name, date, band_name, venue, genre, looking_for)

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
                return {'Gig postings': gig_postings}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_gig(self):
        if cherrypy.request.method == 'POST':
            try:
                input_json = cherrypy.request.json
                gig_name = input_json.get('gig_name')
                date = input_json.get('date')

                gig = self.dynamodb_service.get_gig(gig_name, date)
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
    def update_gig(self, **kwargs):
        if cherrypy.request.method == 'POST':
            try:
                gig_name = kwargs.get('gig_name')
                date = kwargs.get('date')
                update_data = cherrypy.request.json
            
                self.dynamodb_service.update_gig(gig_name, date, **update_data)
                return {'status': 'success', 'message': 'Gig posting updated successfully'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def delete_gig(self):
        if cherrypy.request.method == 'POST':
            try:
                input_json = cherrypy.request.json
                gig_name = input_json.get('gig_name')
                date = input_json.get('date')

                success = self.dynamodb_service.delete_gig(gig_name, date)
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
