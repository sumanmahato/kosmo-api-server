from langchain_core.tools import Tool
import json
import re

def call_query_api(params_str: str) -> str:
    """Call the actual API with structured parameters"""
    try:
        dict_match = re.search(r'\{[^{}]*\}', params_str)
        if dict_match:
            params_dict = eval(dict_match.group())
            
            # abhi ke liye just returning this warna can make api call here...
            result = {
                "status": "success",
                "query_params": params_dict,
                "message": "Query executed successfully"
            }
            
            return f"API call completed successfully. Query parameters: {json.dumps(params_dict, indent=2)}"
        else:
            return "Error: Could not extract parameters from input"
            
    except Exception as e:
        return f"Error calling API: {str(e)}"

api_tool = Tool(
    name="APIProcessor",
    func=call_query_api,
    description=(
        "Use this tool to execute API calls with structured parameters. "
        "Pass the structured parameters obtained from QueryProcessor to this tool. "
        "This tool returns the final result - no further processing is needed."
    ),
)