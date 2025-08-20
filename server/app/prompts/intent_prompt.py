from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.models.ollama_wrapper import get_llm

intent_prompt = PromptTemplate(
    input_variables=["user_input", "history"],
    template="""
Conversation history:
{history}

Classify the intent of the user input as either "da_query", "workflow", or "rag_query".

You are an intelligent assistant designed to classify user queries and route them to the correct processing module.
There are three modules:

- `rag_query`: Use this for general help, FAQs, or questions that are not related to retrieving specific data using queries or creating workflows. For example:
  - General questions about the Komprise product
  - Usage instructions or how-to guides
  - Questions not involving schema fields, filters, or workflow operations
  - If '{user_input}' is a generic question

- `da_query`: Use this when the user is asking to retrieve files, directories, or datasets using metadata filters.
  - Only use `da_query` when it mentions or implies data being retrieved on the basis of schema fields such as:
    `lastModified`, `lastAccessed`, `moved`,
    `fileSizes`, `fileExtensions`, `fileTypes`,
    `fileGroups`, `fileOwners`, `directoryName`, `fileNames`, `filterTags`, `exclusions`

- `workflow`: Use this when the user wants to create, set up, or configure a workflow for data processing or tagging.
  - Use `workflow` when the request involves:
    - Creating workflows for setting up PII tagging or labeling processes
    - Mentions of setting workflows for tagging data with specific labels/keys
  - Examples: "create a workflow to tag PII data", "make a workflow to label data with Project"

---

Now classify the following input.
{user_input}
Only respond with one word: `da_query`, `workflow`, or `rag_query`.
"""
)
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from app.models.ollama_wrapper import get_llm

# intent_prompt = PromptTemplate(
#     input_variables=["user_input", "history"],
#     template="""
# Conversation history:
# {history}

# Classify the intent of the user input as either "da_query" or "rag_query".

# You are an intelligent assistant designed to classify user queries and route them to the correct processing module.
# There are two modules:

# - `rag_query`: Use this for general help, FAQs, or questions that are not related to retrieving specific data using queries. For example:
#   - General questions about the Komprise product
#   - Usage instructions or how-to guides
#   - Questions not involving schema fields or filters
#   - If '{user_input}' is a generic question

# - `da_query`: Use this when the user is asking to retrieve files, directories, or datasets using metadata filters.
#   - Only use `da_query` when it Mentions or implies data being retrieved on the basis of schema fields such as:
#     `lastModified`, `lastAccessed`, `moved`,
#     `fileSizes`, `fileExtensions`, `fileTypes`,
#     `fileGroups`, `fileOwners`, `directoryName`, `fileNames`, `filterTags`, `exclusions`
  

# ---

# ---
# Now classify the following input.
# {user_input}
# Only respond with one word: `da_query` or `rag_query`.
# """
# )
