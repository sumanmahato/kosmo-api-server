# app/utils/response_utils.py
import uuid
import json
from dateutil import parser
from datetime import datetime


def convert_to_ddmmyyyy(dates):
    converted_dates = []
    for date_str in dates:
        try:
            parsed_date = parser.parse(date_str, dayfirst=False)
            formatted_date = parsed_date.strftime('%Y-%m-%d')
            converted_dates.append(formatted_date)
        except (ValueError, TypeError):
            converted_dates.append(f"Invalid date: {date_str}")
    return converted_dates

def _handle_da_query(response: dict) -> tuple[dict, str]:
    """
    Parses DA_QUERY response which is expected to be a JSON dict.

    """
    try:
        filters = response["data"]
        for field_name in ["lastAccessed", "lastModified", "moved"]:
            field_data = filters.get(field_name)
            if field_data and isinstance(field_data, list) and len(field_data) > 0:
                entry = field_data[0]
                if "date" in entry:
                    entry["date"] = convert_to_ddmmyyyy([entry["date"]])[0]
                elif "data" in entry and "_" in entry["data"]:
                    a, b = entry["data"].split("_", 1)
                    a_conv, b_conv = convert_to_ddmmyyyy([a, b])
                    entry["data"] = f"{a_conv}_{b_conv}"

        action_data = {"filters": filters, "tagNames": response["tagNames"]}
        # action_data = {"filters": filters}
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
    response_dict = response["content"]
    if isinstance(response_dict, dict):
        message = response_dict.get("answer", "No answer generated.")
        data = response_dict.get("sources", [])
        resources = [item.get("url", item.get("source")) for item in data if "url" in item or "source" in item]
        print(">>>>>",  data, resources)
    elif hasattr(response_dict, "content"):
        message = response_dict.content
    else:
        message = str(response_dict)
    print("ajfjasfkjalksf>>>>", resources)
    return action_data, resources, message

def _handle_workflow(response: any) -> tuple[dict, str]:
    """
    Parses Workflow response which is expected to be a JSON dict.

    """
    try:
        workflowParams = response["data"]
        workflowIsComplete = response["isConversationComplete"]
        workflowMessage = response["content"]
        action_data = {
            "workflowParams": workflowParams,
            "isComplete": workflowIsComplete
        }
        return action_data, workflowMessage
    
    except json.JSONDecodeError:
        action_data = {}
        message = "Invalid filter format from query agent."

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
        if response["actionType"] == "report":
            action = "REPORT"
    elif action in ("RAG_QUERY", "UNKNOWN"):
        action_data, resources, message = _handle_rag_response(response)
    elif action == "WORKFLOW":
        action_data, message = _handle_workflow(response)

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
