from langchain.chains import RetrievalQA
from app.models.ollama_wrapper import get_llm
from app.tools.rag_tools.vectorstore import load_existing_vectorstore

# Initialize LLM and vector store
llm = get_llm()
vectorstore = load_existing_vectorstore()
retriever = vectorstore.as_retriever()

# Standard RAG Chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True  # Can help in debugging
)

def get_answer(query: str) -> dict:
    """
    Get a RAG-based answer for the given query.
    """
    result = rag_chain.invoke({"query": query})
    return {
        "answer": result.get("result", ""),
        "sources": [doc.metadata for doc in result.get("source_documents", [])]
    }
