from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models.ollama_wrapper import get_llm

intent_prompt = PromptTemplate(
    input_variables=["user_input", "history"],
    template="""
Conversation history:
{history}

Classify the intent of the user input as either "da_query" or "rag_query".

You are an intelligent assistant designed to classify user queries and route them to the correct processing module.
There are two modules:

- `rag_query`: Use this for general help, FAQs, or questions that are not related to retrieving specific data using queries. For example:
  - General questions about the Komprise product
  - Usage instructions or how-to guides
  - Questions not involving schema fields or filters
  - If '{user_input}' is a generic question

- `da_query`: Use this when the user is asking to retrieve files, directories, or datasets using metadata filters. This includes any query that:
  - Only use `da_query` when it Mentions or implies schema fields such as:
    `lastModified`, `lastAccessed`, `moved`,
    `fileSizes`, `fileExtensions`, `fileTypes`,
    `fileGroups`, `fileOwners`, `directoryName`, `fileNames`, `filterTags`, `exclusions`
  

---

---
Now classify the following input.
{user_input}
Only respond with one word: `da_query` or `rag_query`.
"""
)
