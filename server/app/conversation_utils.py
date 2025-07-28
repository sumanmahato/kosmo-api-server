from langchain.memory import ConversationSummaryBufferMemory
from app.models.ollama_wrapper import get_llm

_session_memories = {}

# Tune this as needed (e.g., lower for quicker summarization)
MAX_TOKEN_LIMIT = 100

def get_session_memory(session_id):
    if session_id not in _session_memories:
        _session_memories[session_id] = ConversationSummaryBufferMemory(
            llm=get_llm(),
            max_token_limit=MAX_TOKEN_LIMIT,
            return_messages=True,  # important to access message objects
            memory_key="history"
        )
    return _session_memories[session_id]

def build_context_for_llm(memory):
    """
    Returns list of messages to send to the LLM: summary + recent turns
    """
    summary = memory.moving_summary_buffer
    recent_messages = memory.chat_memory.messages

    context = []
    if summary:
        context.append({"role": "system", "content": summary})

    context += [
        {"role": msg.type, "content": msg.content}
        for msg in recent_messages
    ]

    return context

def extract_summary_and_history(messages: list[dict]):
    summary = ""
    history = []

    for msg in messages:
        if msg["role"] == "system" and not summary:
            summary = msg["content"]
        else:
            history.append(msg)
    
    return summary, history