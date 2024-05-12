import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
import json
import os
from collections import defaultdict
from services.message_service import MessageService

def cors_tool():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'

cherrypy.tools.cors = cherrypy.Tool('before_finalize', cors_tool, priority=60)

class ChatWebSocketHandler(WebSocket):
    clients = defaultdict(set)

    def received_message(self, message):
        message_service = MessageService()
        data = json.loads(message.data.decode('utf-8'))
        action = data.get('action')

        if action == 'join':
            chat_id = data.get('chat_id', "")
            print(chat_id)
            self.clients[chat_id].add(self)
        elif action == 'leave':
            chat_id = data.get('chat_id', "")
            if self in self.clients[chat_id]:
                self.clients[chat_id].remove(self)
        elif action == 'message':
            chat_id = data['chat_id']
            username = data['username']
            message_text = data['message']
            message_id = message_service.send_message(chat_id, username, message_text)
            print(self.clients[chat_id])
            for client in self.clients[chat_id]:
                client.send(message)

    def closed(self, code, reason=None):
        for clients in self.clients.values():
            clients.discard(self)

    def opened(self):
        print("WebSocket connection opened.")

class MessageController:
    def __init__(self):
        self.message_service = MessageService()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.tools.cors()
    def create_chat(self):
        if cherrypy.request.method == 'POST':
            input_data = cherrypy.request.json
            chat_id = self.message_service.create_chat(input_data['usernames'], input_data['chat_name'], input_data.get('is_group', False))
            return {"chat_id": chat_id}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_user_chats(self):
        if cherrypy.request.method == 'POST':
            input_data = cherrypy.request.json
            chats = self.message_service.get_user_chats(input_data['username'])
            return {"chats": chats}
        return ''

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.cors()
    def get_messages(self):
        if cherrypy.request.method == 'POST':
            input_data = cherrypy.request.json
            messages = self.message_service.get_messages(input_data['chat_id'])
            return {"messages": messages}
        return ''

    @cherrypy.expose
    def ws(self):
        handler = cherrypy.request.ws_handler


if __name__ == '__main__':
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    config = {
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': ChatWebSocketHandler
        },
        '/': {
            'tools.sessions.on': True,
            'tools.cors.on': True 
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8091})
    cherrypy.quickstart(MessageController(), '/', config)
