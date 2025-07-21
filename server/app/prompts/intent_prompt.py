from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models.ollama_wrapper import get_llm

intent_prompt = PromptTemplate(
    input_variables=["user_input", "history"],
    template="""
Conversation history:
{history}

Classify the intent of the user input.

Input: "{user_input}"

Does this input require processing a data query (like finding data, retrieving filtered results, or searching for specific metrics)?
If the input has anything to do with data or operations on it respond with "da_query"
If the input doesnt have anything to do with data or queries respond with "unknown".
"""
)
