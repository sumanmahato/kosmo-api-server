from app.tools.query_tool import query_tool
from app.agents.query_agent import get_llm
import json
import re



class QueryProcessorAgent:
    def __init__(self):
        self.llm = get_llm()
        self.query_tool = query_tool
    
    def run(self, inputs: dict) -> str:
        """Execute the simple two-step query and api pipeline"""
        user_input = inputs["user_input"]
        history = inputs.get("history", "")

        try:
            
            print("[DEBUG] Step 1: Extracting query parameters...")
            query_result = self.query_tool.func(user_input, self.llm, history)
            print(f"[DEBUG] Query result: {query_result}")

            # print("[DEBUG] Step 2: Calling API...")
            # api_result = self.api_tool.func(query_result)
            # print(f"[DEBUG] API result: {api_result}")
            
            return query_result
            
        except Exception as e:
            return f"Error in query processing: {str(e)}"

def get_query_processing_agent():
    return QueryProcessorAgent()
