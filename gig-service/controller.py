import cherrypy
from services.dynamodb_service import DynamoDBService

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
    def post_gig(self):
        try:
            input_json = cherrypy.request.json
            gig_name = input_json.get('GigName')
            date = input_json.get('Date')
            band_name = input_json.get('BandName')
            venue = input_json.get('Venue')
            genre = input_json.get('Genre')
            looking_for = input_json.get('LookingFor')

            self.dynamodb_service.create_gig(gig_name, date, band_name, venue, genre, looking_for)
            return {'status': 'success', 'message': 'Gig creation successful.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_gig_postings(self):
        gig_postings = self.dynamodb_service.scan_table()
        return {'Gig postings': gig_postings}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_gig(self, gig_name, date):
        gig = self.dynamodb_service.get_gig(gig_name, date)
        if gig:
            return {'status': 'success', 'gig': gig}
        else:
            return {'status': 'error', 'message': 'Gig not found'}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def update_gig(self, **kwargs):
        gig_name = kwargs.get('gig_name')
        date = kwargs.get('date')
        update_data = cherrypy.request.json
        
        try:
            self.dynamodb_service.update_gig(gig_name, date, **update_data)
            return {'status': 'success', 'message': 'Gig posting updated successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete_gig(self, gig_name, date):
        success = self.dynamodb_service.delete_gig(gig_name, date)
        if success:
            return {'status': 'success', 'message': 'Gig deleted successfully'}
        else:
            return {'status': 'error', 'message': 'Failed to delete gig'}


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8082})
    cherrypy.quickstart(GigService())
