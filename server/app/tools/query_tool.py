from langchain.output_parsers import PydanticOutputParser
from app.prompts.query_prompt import query_prompt
from langchain_core.tools import Tool
from app.schemas.query_schema import QueryParams
from app.models.ollama_wrapper import get_llm
from mlx_lm import generate
from pydantic import BaseModel, Field

parser = PydanticOutputParser(pydantic_object=QueryParams)

def query_pipeline(user_input: str, llm: (), history: str = "") -> str:
    """Extract structured parameters from user input"""
    model, tokenizer = llm
    history.append({"role": "user", "content": user_input})
    inputs = history

    try:
        text = tokenizer.apply_chat_template(
            inputs,
            tokenize=False,
            add_generation_prompt=True
        )
        response = generate(model, tokenizer, prompt=text, verbose=True, max_tokens=512)
        return f"{response}"
    except Exception as e:
        return f"Error parsing query: {str(e)}"

query_tool = Tool(
    name="QueryProcessor",
    func=query_pipeline,
    description=(
        "Use this to extract structured parameters from natural language queries. "
        "This tool extracts query parameters like tier, volume, and date_range. "
        "After getting the parameters, use the APIProcessor tool to execute the query."
    ),
)