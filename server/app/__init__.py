from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret'

    socketio.init_app(app)

    # Register other routes or blueprints if needed
    from app import socket_event  # this registers the handlers

    return app
