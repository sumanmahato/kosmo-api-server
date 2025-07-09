from langchain.agents import Tool, initialize_agent, AgentType
from langchain_core.tools import tool
from models.ollama_wrapper import get_llm

def call_backend_api(params: dict) -> str:
    return f"API called with: {params}"
    # yaha se client?

@tool
def api_handler_tool(params: dict) -> str:
    """Takes structured query data and creates an API call."""
    return call_backend_api(params)

def get_api_agent():
    llm = get_llm()

    return initialize_agent(
        tools=[api_handler_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
