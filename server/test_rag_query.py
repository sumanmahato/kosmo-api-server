from app.models.ollama_wrapper import get_llm
from app.tools.vectorstore_loader import load_existing_vectorstore
from langchain.chains import RetrievalQA

try:
    # Load LLM and vectorstore
    print("🔧 Loading LLM and vectorstore...")
    llm = get_llm()
    vectorstore = load_existing_vectorstore()
    retriever = vectorstore.as_retriever()

    # Create a RAG chain
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Run test query
    query = "what is komprise?"
    print(f"\n🔍 Querying: {query}")
    response = rag_chain.run(query)
    print(f"\n📄 Response:\n{response}")

except Exception as e:
    print(" Error occurred:", e)

