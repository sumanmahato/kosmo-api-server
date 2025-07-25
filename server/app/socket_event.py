from flask import request
from app import socketio
import uuid

from app.router.intent_router import route_intent
from app.conversation_utils import get_conversation_history, save_conversation_history
# from app.agents.query_agent import get_query_agent
# from app.agents.query_agent import handle_query  # example
# or from app.tools.query_tool import run_query  # depending on your usage

MAX_HISTORY = 10 # Number of messages before summarizing
RECENT_HISTORY = 3  # Number of recent messages to keep after summarizing

@socketio.on('connect')
def on_connect():
    print(f"Client connected: {request.sid}")
    socketio.emit('server_message', {'message': 'Connected successfully'})

@socketio.on('user-message')
def on_user_message(data):
    print(f"Received user message: {data}")
    message = data.get("message", "")
    session_id = request.sid

    # Retrieve and update session memory
    conversation = get_conversation_history(session_id)
    memory = conversation["memory"]
    summary = conversation["summary"]
    memory.append({"role": "user", "content": message['content']})

    # --- Summarization logic ---
    if len(memory) > MAX_HISTORY:
        from app.chains.summarize_chain import summarize_chain, format_history_for_summary
        summary_result = summarize_chain.invoke({"history": format_history_for_summary(memory)})

        if isinstance(summary_result, dict) and 'text' in summary_result:
            summary = summary_result['text']
        else:
            summary = str(summary_result)

        # Keep only the most recent RECENT_HISTORY messages
        memory = memory[-RECENT_HISTORY:]
        print(f"[DEBUG] Memory: {memory}")
        print(f"[DEBUG] Summary: {summary}")

    # Prepare context: summary + recent memory
    context_memory = memory[-RECENT_HISTORY:]
    
    # Pass context to route_intent
    agentResponse = route_intent(message['content'], memory=context_memory, summary=summary)

    memory.append({"role": "system", "content": agentResponse})
    save_conversation_history(session_id, memory, summary)



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
    print(response)
    socketio.emit('system-message', response, room=request.sid)

@socketio.on('disconnect')
def on_disconnect():
    print(f"Client disconnected: {request.sid}")
