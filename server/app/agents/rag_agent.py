from langchain.chains import RetrievalQA
from app.models.ollama_wrapper import get_llm
from app.tools.rag_tools.vectorstore import load_existing_vectorstore
from app.agents.rag_pipline import RAGPipeline

# # Initialize LLM and vector store
# rag_llm = get_llm()
# vectorstore = load_existing_vectorstore()
# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# # Standard RAG Chain
# rag_chain = RetrievalQA.from_chain_type(
#     llm=rag_llm,
#     retriever=retriever,
#     return_source_documents=True, # Can help in debugging
# )

def get_answer(query: str, history: str, summary: str) -> dict:
    """
    Get a RAG-based answer for the given query, incorporating summary and history. Use "[User Question]" for query
    """

    pipeline = RAGPipeline()
    
    result = pipeline.run(query, summary, history)

    return {
        "answer": result.get("answer", ""),
        "sources": result.get("sources", [])
    }
