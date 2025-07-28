from langchain.prompts import PromptTemplate


# Define custom prompt with summary and history included
rag_prompt = PromptTemplate.from_template("""
You are an assistant answering user questions using provided documents and context.

Summary of conversation so far:
{summary}

Recent messages:
{history}

Relevant documents:
{context}

User question:
{query}

Answer:
""")
