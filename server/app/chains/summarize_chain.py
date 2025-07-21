from langchain.chains import LLMChain

from app.prompts.summary_prompt import summary_prompt
from app.models.ollama_wrapper import get_llm

def format_history_for_summary(memory):
    """Format the memory list into a string for summarization."""
    return "\n".join([f"{m['role']}: {m['content']}" for m in memory])

llm = get_llm()
summarize_chain = LLMChain(llm=llm, prompt=summary_prompt)