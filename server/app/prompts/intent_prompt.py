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
- `da_query`: Use this when the user is asking about files, directories, or datasets using metadata filters. This includes any query that:
  - Mentions or implies schema fields such as:
    `lastModified`, `lastAccessed`, `moved`,
    `fileSizes`, `fileExtensions`, `fileTypes`,
    `fileGroups`, `fileOwners`, `directoryName`, `fileNames`, `filterTags`, `exclusions`
  - Refers to filtering, selecting, summarizing, or inspecting files/groups/directories using conditions or keywords such as:
    "modified", "accessed", "name contains", "ends with", "owner includes", "path starts with", "files with extension", etc.
- `rag_query`: Use this for general help, FAQs, or queries that are not related to file filtering or metadata-based search. For example:
  - General questions about the Komprise product
  - Usage instructions or how-to guides
  - Questions not involving schema fields or filters
---

---
Now classify the following input.
{user_input}
Only respond with one word: `da_query` or `rag_query`.
"""
)
