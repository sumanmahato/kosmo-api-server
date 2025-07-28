from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models.ollama_wrapper import get_llm

intent_prompt = PromptTemplate(
    input_variables=["user_input", "history"],
    template="""
Conversation history:
{history}

Classify the intent of the user input as either "da_query" or "rag_query".

Input: "{user_input}"

- da_query: Use this label **only if** the input is asking to perform a **process a data query**, such as:
  - finding query data
  - retrieving filtered results
  - searching for specific metrics

- rag_query: Use this label for all other inputs, including:
  - general questions about komprise
  - komprise product documentation, features, and how it works
  - komprise knowledge-based or FAQ-style queries

If the input does not clearly match the definition of a da_query, default to rag_query.

Only respond with one word: da_query or rag_query
"""
)
