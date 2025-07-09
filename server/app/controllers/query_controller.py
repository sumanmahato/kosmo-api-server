from app.tools.query_tool import query_pipeline
from app.agents.api_agent import get_api_agent

def handle_query_to_api(user_input: str):
    query_params = query_pipeline(user_input)  
    api_agent = get_api_agent()               
    return api_agent.run(query_params)
