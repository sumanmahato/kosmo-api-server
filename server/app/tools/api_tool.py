def mock_api_call(params: dict):
    # Mock response
    return f"Query executed with params: {params}"

from langchain.tools import Tool

api_tool = Tool(
    name="ExecuteQueryAPI",
    func=mock_api_call,
    description="Executes a structured internal query via API",
)
