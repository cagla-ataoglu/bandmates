import cherrypy
from services.dynamodb_service import DynamoDBService

class ProfileService:

    def __init__(self):
        self.dynamodb_service = DynamoDBService()

    @cherrypy.expose
    @cherrypy.tools.json_out
    def index(self):
        return {"message": "Welcome to Profile Service"}
