from flask import request
from app import socketio
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
    user_id = data.get("userId", "anonymous")

    # 🔁 route message to your agent / tool / prompt
    response = {
        "message": f"You said: {message}",
        "action": {
            "type": "API",
            "actionId": "mock_action",
            "metadata": {
                "userId": user_id
            }
        }
    }

    # 🔄 send response back
    socketio.emit('system-message', "You said: {message}")

@socketio.on('disconnect')
def on_disconnect():
    print(f"Client disconnected: {request.sid}")
