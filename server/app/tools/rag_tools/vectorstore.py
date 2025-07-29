from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from .embeddings import get_embeddings
import json

CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "kosmo-rag-db"

def embed_documents_to_chroma(documents, persist_dir=CHROMA_DB_DIR, batch_size=64):
    """
    Split documents into chunks and store them in Chroma vector DB.
    """
    print("[INFO] Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)
    print(f"[INFO] Split into {len(split_docs)} chunks.")

    embeddings = get_embeddings()
    Chroma.from_documents(split_docs, embeddings, persist_directory=persist_dir, collection_name=COLLECTION_NAME)
    print(f"[INFO] Chunks added to vectorstore at {persist_dir}")


def load_existing_vectorstore(persist_dir=CHROMA_DB_DIR, collection_name=COLLECTION_NAME):
    """
    Load an existing Chroma vectorstore for retrieval.
    """
    embeddings = get_embeddings()
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings,  collection_name=collection_name)
    print(f"[INFO] Loaded existing vectorstore from '{persist_dir}'")
    return vectorstore


def sanitize_metadata(metadata: dict) -> dict:
    """
    Convert complex metadata values (lists, dicts) to JSON strings
    since Chroma only accepts str, int, float, bool, or None.
    """
    clean_metadata = {}
    for key, value in metadata.items():
        if isinstance(value, (list, dict)):
            clean_metadata[key] = json.dumps(value)
        else:
            clean_metadata[key] = value
    return clean_metadata


def push_freshdesk_artices_to_chroma(docs):
    embeddings = get_embeddings()
    langchain_docs = [
        Document(page_content=d["text"], metadata=sanitize_metadata(d["metadata"])) for d in docs
    ]
    Chroma.from_documents(
        langchain_docs,
        embeddings,
        persist_directory=CHROMA_DB_DIR,
        collection_name=COLLECTION_NAME
    )
    print(f"[INFO] Pushed {len(langchain_docs)} documents to ChromaDB.")