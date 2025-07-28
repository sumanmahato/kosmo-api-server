# app/utils/response_utils.py
import uuid
import json

def _handle_da_query(response: str) -> tuple[dict, str]:
    """
    Parses DA_QUERY response which is expected to be a JSON string.

    Returns:
        (action_data, message)
    """
    try:
        filters = json.loads(response)
        action_data = {"filters": filters}
        message = (
            "Your filters have been applied and the query is ready. "
            "You can now view, explore, or analyze the matching data."
        )
    except json.JSONDecodeError:
        action_data = {}
        message = "Invalid filter format from query agent."
    return action_data, message


def _handle_rag_response(response: any) -> tuple[dict, list, str]:
    """
    Parses RAG/UNKNOWN response which is expected to be a dict or LLM result.

    Returns:
        (action_data, resources, message)
    """
    action_data = {}
    resources = []
    message = ""

    if isinstance(response, dict):
        message = response.get("answer", "No answer generated.")
        resources = response.get("sources", [])
    elif hasattr(response, "content"):
        message = response.content
    else:
        message = str(response)

    return action_data, resources, message


def get_response_content(response, intent_type: str = "UNKNOWN") -> dict:
    """
    Constructs a structured socket message for the frontend.

    Args:
        response (Any): Raw output from agent.
        intent_type (str): 'DA_QUERY', 'RAG_QUERY', or 'UNKNOWN'.

    Returns:
        dict: Standardized socket message format.
    """
    print(f"[RESPONSE] Processing response with intent type: {intent_type}")

    action = intent_type.upper() if intent_type else "UNKNOWN"
    message_id = str(uuid.uuid4())
    action_data = {}
    resources = []
    message = ""

    if action == "DA_QUERY":
        action_data, message = _handle_da_query(response)

    elif action in ("RAG_QUERY", "UNKNOWN"):
        action_data, resources, message = _handle_rag_response(response)

    else:
        message = str(response)

    return {
        "role": "system",
        "content": {
            "action": action,
            "action_data": action_data,
            "resources": resources,
            "message": message.strip()
        },
        "id": message_id
    }
