from langchain_core.tools import Tool
import json
import re

def call_query_api(params_str: str) -> str:
    """Display structured parameters instead of actually calling API"""
    print("received", params_str)
    return f"{params_str}"


api_tool = Tool(
    name="APIProcessor",
    func=call_query_api,
    description=(
        "Use this tool to execute API calls with structured parameters. "
        "Pass the structured parameters obtained from QueryProcessor to this tool. "
        "This tool returns the final result - no further processing is needed."
    ),
)