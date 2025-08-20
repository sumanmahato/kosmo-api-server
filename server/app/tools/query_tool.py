from app.prompts.query_prompt import query_prompt
from langchain_core.tools import Tool
from app.schemas.query_schema import QueryParams
from app.models.ollama_wrapper import get_llm
from mlx_lm import generate
from pydantic import BaseModel, Field


def should_include_history(user_input: str) -> bool:
    user_input = user_input.lower()
    return any(
        phrase in user_input
        for phrase in [
            "add", "append", "also", "in addition", "along with", "plus", "refine", "update", "modify", "build on"
        ]
    )

def build_workflow_config(extracted_params: dict) -> dict:
    """Build the complete workflow configuration"""
    return {
        "content": "Completed query has been created",
        "classifier": "da_query",
        "isConversationComplete": True,
        "data": extracted_params        
    }

def query_pipeline(user_input: str, llm: (), history: str) -> dict:
    """Extract structured parameters from user input"""
    model, tokenizer = llm
    if should_include_history(user_input): 
        print("IJADBFJBAIBABAJFDBJKADBFJKFBADKJBF")
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
        return build_workflow_config(response)
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