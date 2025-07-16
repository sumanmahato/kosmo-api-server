from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models.ollama_wrapper import get_llm

intent_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
Classify the intent of the user input.

Input: "{user_input}"

Does this input require processing a data query (like finding data, retrieving filtered results, or searching for specific metrics)?
If the input has anything to do with data or operations on it respond with "da_query"
If the input is a knowledge-based question related to the following topics: LangChain, Komprise, or Ollama, respond with "rag_query"
If it doesn't fall into either of these categories, respond with "unknown"
"""
)
