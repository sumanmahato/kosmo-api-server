from app.tools.query_tool import query_tool
from app.models.ollama_wrapper import get_llm
from langchain.agents import initialize_agent, AgentType

def get_query_agent():
    llm = get_llm()
    
    return initialize_agent(
        tools=[query_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
