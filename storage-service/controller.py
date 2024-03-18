import cherrypy
from services.storage_service import StorageService
import os

class StorageController:

    def __init__(self):
        self.storage_service = StorageService()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self, media):
        if not media:
            return {"error": "No file uploaded"}

        file_name = media.filename
        file_content = media.file
        file_url = self.storage_service.upload_media(file_content, file_name)
        return {"message": "Upload successful", "url": file_url}

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8082})
    cherrypy.quickstart(StorageController())
