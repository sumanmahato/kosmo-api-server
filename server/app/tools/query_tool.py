from langchain.output_parsers import PydanticOutputParser
from app.prompts.query_prompt import query_prompt
from langchain_core.tools import Tool
from app.schemas.query_schema import QueryParams
from app.models.ollama_wrapper import get_llm

parser = PydanticOutputParser(pydantic_object=QueryParams)

def call_query_api(params: dict):
    return f"Query executed with params: {params}"

def query_pipeline(user_input: str) -> str:
    llm = get_llm()
    chain = query_prompt | llm | parser
    structured = chain.invoke({"query": user_input})
    result = call_query_api(structured.dict())
    return f"{result}"

# def query_pipeline(user_input: str) -> dict:
#     llm = get_llm()
#     chain = query_prompt | llm | parser
#     structured = chain.invoke({"query": user_input})
#     return structured.dict()  


query_tool = Tool(
    name="QueryProcessor",
    func=query_pipeline,
    description=(
        "Use this to process natural language queries. "
        "This tool immediately returns the result — no further action is needed. "
    ),
)

