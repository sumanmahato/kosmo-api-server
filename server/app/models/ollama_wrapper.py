from langchain_community.chat_models import ChatOllama

def get_llm():
    return ChatOllama(model="mistral", temperature=0)


def get_llm_qwen():
    return ChatOllama(
        model="qwen2.5:3b",  # Instruction-tuned by default
        temperature=0.1
    )
