from app.prompts.query_prompt import query_prompt
from langchain_core.tools import Tool
from app.schemas.query_schema import QueryParams
# from app.models.ollama_wrapper import get_llm
from mlx_lm import generate
from pydantic import BaseModel, Field
from app.tools.reports_helper import get_report_params
import re
import json


def should_include_history(user_input: str) -> bool:
    user_input = user_input.lower()
    return any(
        phrase in user_input
        for phrase in [
            "add", "append", "also", "in addition", "along with", "plus", "refine", "update", "modify", "build on"
        ]
    )

def build_da_config(extracted_params: dict, reports_params: dict) -> dict:
    """Build the complete da configuration"""
    return {
        "content": "Completed query has been created",
        "classifier": "da_query",
        "isConversationComplete": True,
        "data": extracted_params,
        "tagNames": reports_params.get("tagNames", []),
        "actionType": reports_params.get("reports", "")      
    }

def handle_reports(user_input: str) -> tuple:
    reports_params = get_report_params(user_input)
    cleaned_query = user_input
    cleaned_query = re.sub(r"(tagged with|having tags?|with tags?)\s+[^,.;]*", "", cleaned_query, flags=re.IGNORECASE)
    if reports_params and "tagNames" in reports_params:
        tag_values = reports_params["tagNames"]
        if isinstance(tag_values, str):
            tag_values = [tag_values]
        for tag in tag_values:
            if tag:
                cleaned_query = re.sub(rf"\b{re.escape(tag)}\b", "", cleaned_query, flags=re.IGNORECASE)

    cleaned_query = " ".join(cleaned_query.split())
    new_reports_params = {
        "reports": None,
        "tagNames": []
    }

    if(reports_params.get('actionType') == 'report'):
        new_reports_params["reports"] = "report"
    new_reports_params["tagNames"] = reports_params.get("tagNames", [])
    return new_reports_params, cleaned_query
    

def query_pipeline(user_input: str, llm: (), history: str) -> dict:
    """Extract structured parameters from user input"""
    model, tokenizer = llm
    reports_params, cleaned_query = handle_reports(user_input)
    print("TESTESTESTEST", reports_params, cleaned_query)
    user_input = cleaned_query
    if should_include_history(user_input): 
        inputs = [{"role": "user", "content": f'''use "{history}" as history to construct {user_input} '''}]
    else:
        inputs = [{"role": "user", "content": user_input}]

    try:
        text = tokenizer.apply_chat_template(
            inputs,
            tokenize=False,
            add_generation_prompt=True
        )
        response = generate(model, tokenizer, prompt=text, verbose=True, max_tokens=512)
        return build_da_config(json.loads(response), reports_params)
    except Exception as e:
        return {"error": e}

query_tool = Tool(
    name="QueryProcessor",
    func=query_pipeline,
    description=(
        "Use this to extract structured parameters from natural language queries. "
        "This tool extracts query parameters like tier, volume, and date_range. "
        "After getting the parameters, use the APIProcessor tool to execute the query."
    ),
)