import json
import os

CONVERSATIONS_FILE = "conversations.json"

def load_conversations():
    if not os.path.exists(CONVERSATIONS_FILE):
        return {}
    with open(CONVERSATIONS_FILE, "r") as f:
        return json.load(f)

def save_conversations(conversations):
    with open(CONVERSATIONS_FILE, "w") as f:
        json.dump(conversations, f, indent=2)

def get_conversation_history(session_id):
    conversations = load_conversations()
    return conversations.get(session_id, {"memory": [], "summary": ""})

def save_conversation_history(session_id, memory, summary):
    conversations = load_conversations()
    conversations[session_id] = {"memory": memory, "summary": summary}
    save_conversations(conversations) 

def build_history(summary, memory):
    lines = []
    if summary:
        lines.append(summary)
    if memory:
        lines.extend(f"{m['role']}: {m['content']}" for m in memory)
    return "\n".join(lines).strip()
