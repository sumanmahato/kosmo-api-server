from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .embeddings import get_embeddings

CHROMA_DB_DIR = "chroma_db"

def embed_documents_to_chroma(documents, persist_dir=CHROMA_DB_DIR, batch_size=64):
    """
    Split documents into chunks and store them in Chroma vector DB.
    """
    print("[INFO] Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)
    print(f"[INFO] Split into {len(split_docs)} chunks.")

    embeddings = get_embeddings()
    Chroma.from_documents(split_docs, embeddings, persist_directory=persist_dir)
    print(f"[INFO] Chunks added to vectorstore at {persist_dir}")


def load_existing_vectorstore(persist_dir=CHROMA_DB_DIR):
    """
    Load an existing Chroma vectorstore for retrieval.
    """
    embeddings = get_embeddings()
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    print(f"[INFO] Loaded existing vectorstore from '{persist_dir}'")
    return vectorstore
