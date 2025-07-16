# app/models/embedding_wrapper.py

from langchain_community.embeddings import OllamaEmbeddings  # ✅ Updated import!

def get_embedding_model(model_name: str = "nomic-embed-text"):
    return OllamaEmbeddings(model=model_name)