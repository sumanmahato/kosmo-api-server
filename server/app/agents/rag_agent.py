from langchain.chains import RetrievalQA
from app.models.ollama_wrapper import get_llm
from app.tools.rag_tools.vectorstore import load_existing_vectorstore

# Initialize LLM and vector store
rag_llm = get_llm()
vectorstore = load_existing_vectorstore()
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Standard RAG Chain
rag_chain = RetrievalQA.from_chain_type(
    llm=rag_llm,
    retriever=retriever,
    return_source_documents=True, # Can help in debugging
)

def get_answer(query: str, history: str, summary: str) -> dict:
    """
    Get a RAG-based answer for the given query, incorporating summary and history. Use "[User Question]" for query
    """


    # Format input string
    full_query = f"""
    [Conversation Summary]
    {summary}

    [Conversation History]
    {history}

    [User Question]
    {query}
    """

    print(f"[RAG] Full Query:\n{full_query.strip()}")

    result = rag_chain.invoke({"query": full_query.strip()})

    # Log number of retrieved chunks
    print(f"Number of retrieved chunks: {len(result.get('source_documents', []))}")
    
    # Log relevant chunks
    for i, doc in enumerate(result.get('source_documents', []), 1):
        print(f"\n[CHUNK {i}]")
        print(doc.page_content)
        print(f"[Source] {doc.metadata.get('source', 'Unknown')}\n")

    return {
        "answer": result.get("result", ""),
        "sources": [doc.metadata for doc in result.get("source_documents", [])]
    }
