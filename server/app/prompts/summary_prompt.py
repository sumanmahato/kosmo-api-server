from langchain.prompts import PromptTemplate

summary_prompt = PromptTemplate(
    input_variables=["history"],
    template="""
Given the following conversation history between a user and an AI assistant, provide a concise summary that captures the key points, topics discussed, and any important context that should be remembered for future interactions.

Conversation history:
{history}

Summary:
"""
) 