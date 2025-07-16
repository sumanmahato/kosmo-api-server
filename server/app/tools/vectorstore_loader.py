from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
    UnstructuredMarkdownLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.models.embedding_wrapper import get_embedding_model

# Optional: Configure via env
CHROMA_DB_DIR = "db"
EMBED_MODEL = "nomic-embed-text"

def load_documents_from_directory(source_dir: str):
    """
    Load documents (PDFs, .txt, .md) from a given directory.
    """
    loaders = [
        DirectoryLoader(source_dir, glob="**/*.txt", loader_cls=TextLoader),
        DirectoryLoader(source_dir, glob="**/*.pdf", loader_cls=PyPDFLoader),
        DirectoryLoader(source_dir, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader),
    ]
    
    all_docs = []
    for loader in loaders:
        docs = loader.load()
        all_docs.extend(docs)
    
    print(f"[INFO] Loaded {len(all_docs)} documents from {source_dir}")
    return all_docs


def split_documents(documents, chunk_size=200, chunk_overlap=20, separators=["\n\n", "\n", ".", " "]):
    """
    Split documents into chunks for embedding.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=separators)
    split_docs = splitter.split_documents(documents)
    print(f"[INFO] Split into {len(split_docs)} chunks")
    return split_docs


def build_vectorstore(source_dir: str, persist_dir: str = CHROMA_DB_DIR, embed_model: str = EMBED_MODEL):
    """
    Load, split, embed, and persist documents to Chroma vectorstore.
    """
    documents = load_documents_from_directory(source_dir)
    split_docs = split_documents(documents)

    embeddings = get_embedding_model(embed_model)
    
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    vectorstore.persist()
    print(f"[INFO] Vectorstore built and saved to '{persist_dir}'")

    return vectorstore


def load_existing_vectorstore(persist_dir: str = CHROMA_DB_DIR, embed_model: str = EMBED_MODEL):
    """
    Load an existing Chroma vectorstore for retrieval.
    """
    embeddings = get_embedding_model(embed_model)
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    print(f"[INFO] Loaded existing vectorstore from '{persist_dir}'")
    return vectorstore
