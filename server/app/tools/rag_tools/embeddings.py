from app.models.embedding_wrapper import get_embedding_model

# Default embedding model
EMBED_MODEL = "nomic-embed-text"

def get_embeddings(model_name=EMBED_MODEL):
    """
    Load and return the embedding model.
    """
    return get_embedding_model(model_name)
