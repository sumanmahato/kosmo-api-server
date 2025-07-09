from flask import request
from app import socketio
import uuid

from app.router.intent_router import route_intent
# from app.agents.query_agent import get_query_agent
# from app.agents.query_agent import handle_query  # example
# or from app.tools.query_tool import run_query  # depending on your usage

@socketio.on('connect')
def on_connect():
    print(f"Client connected: {request.sid}")
    socketio.emit('server_message', {'message': 'Connected successfully'})

@socketio.on('user-message')
def on_user_message(data):
    print(f"Received user message: {data}")

    message = data.get("message", "")
    # user_id = data.get("userId", "anonymous")
   
    agentResponse = route_intent(message['content'])

    response = {
        "content": agentResponse,
        "type": "system",
        "id": str(uuid.uuid4())
        # "action": {
        #     "type": "API",
        #     "actionId": "mock_action",
        #     "metadata": {
        #         "userId": user_id
        #     }
        # }
    }

    # 🔄 send response back
    socketio.emit('system-message', response)

@socketio.on('disconnect')
def on_disconnect():
    print(f"Client disconnected: {request.sid}")
