from langchain.output_parsers import PydanticOutputParser
from app.prompts.query_prompt import query_prompt
from langchain_core.tools import Tool
from app.schemas.query_schema import QueryParams
from app.models.ollama_wrapper import get_llm
from pydantic import BaseModel, Field

parser = PydanticOutputParser(pydantic_object=QueryParams)

def query_pipeline(user_input: str) -> str:
    """Extract structured parameters from user input"""
    llm = get_llm()
    chain = query_prompt | llm | parser
    
    try:
        structured = chain.invoke({"query": user_input})
        return f"Successfully extracted query parameters: {structured.dict()}"
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