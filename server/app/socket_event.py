from flask import request
from app import socketio
import uuid

from app.router.intent_router import route_intent
from app.conversation_utils import extract_summary_and_history, get_session_memory, build_context_for_llm
from app.utils import get_response_content
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
    user_input = data.get("message", "")
    session_id = request.sid

    memory = get_session_memory(session_id)

    # Step 1: Save user input with empty output
    memory.save_context({"input": user_input['content']}, {"output": ""})

    # Step 2: Build full context (summary + recent messages)
    context_for_llm = build_context_for_llm(memory=memory)
    summary, history = extract_summary_and_history(context_for_llm)

    # Step 3: Run the agent with full memory context
    agent_response, intent = route_intent(user_input['content'], summary=summary, history=history)

    # Step 4: Fill the last assistant message with the actual response
    memory.chat_memory.messages[-1].content = agent_response
    # Debugging
    print(f"[DEBUG] Summary: {memory.moving_summary_buffer}")
    print(f"[DEBUG] Recent: {[m.content for m in memory.chat_memory.messages]}")

    response =  get_response_content(agent_response, intent)
    # 🔄 send response back
    print(response)
    socketio.emit('system-message', response, room=request.sid)

@socketio.on('disconnect')
def on_disconnect():
    print(f"Client disconnected: {request.sid}")
