# app/agents/workflow_agent.py
from app.tools.workflow_tool import workflow_tool
from app.models.ollama_wrapper import get_llm
import json

class WorkflowProcessorAgent:
    def __init__(self):
        self.llm = get_llm()
        self.workflow_tool = workflow_tool
    
    def run(self, inputs: dict, history: list, summary: str) -> dict:
        """Execute the workflow creation pipeline"""
        
        print("WORKFLOW INPUT", inputs)
        user_input = inputs["user_input"]
        query_id = inputs.get("query_id", "1605")

        # mock_summary = "The human asks the AI to find directory paths where the path contains 'img'. The AI provides a response with various filters and conditions for searching files, specifically focusing on directories containing 'img' in their names."
        # mock_history = [
        #     {"role": "human", "content": "locate directory paths with substring img_1", "classifier": "da_query"},
        #     {"role": "ai", "content": "system response", "classifier": "da_query"},
        #     {"role": "human", "content": "create workflow for PII files and name it us-license", "classifier": "workflow"},
        #     {"role": "ai", "content": {"data": {"workflowServiceClass": "PII", "tagKey": "", "displayName": "us-license"}, "response": "tag key is missing, please provide it"}, "classifier": "workflow", "isConversationComplete": False}
        # ]

        try:
            print("[DEBUG] Step 1: Extracting workflow parameters...")
            workflow_result = self.workflow_tool.func(
                user_input,
                self.llm,
                query_id,
                summary,
                history
            )
            print(f"[DEBUG] Workflow result: {workflow_result}")
            
            return workflow_result
            
        except Exception as e:
            return f"Error in workflow processing: {str(e)}"


def get_workflow_processing_agent():
    return WorkflowProcessorAgent()
