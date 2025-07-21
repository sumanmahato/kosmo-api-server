from app.agents.query_agent import get_query_agent
from app.models.ollama_wrapper import get_llm
from app.prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain, RetrievalQA

from app.tools.vectorstore_loader import load_existing_vectorstore

llm = get_llm()
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

# Load vectorstore + setup retriever and RAG chain
vectorstore = load_existing_vectorstore()
retriever = vectorstore.as_retriever(search_type="similarity")
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def route_intent(user_input: str):
    response = rag_chain.invoke({"query": user_input})
    print("[RAG] Response:", response)
    return response["result"]
    classification = intent_chain.run({"user_input": user_input}).strip().lower()
    print(f"[DEBUG] Raw classification: {repr(classification)}")

    if "da_query" in classification:
        agent = get_query_agent()
        return agent.run(user_input)
    elif "rag_query" in classification:
        docs = retriever.get_relevant_documents(user_input)
        if docs:
            print(f"[RAG] Found {len(docs)} relevant documents.")

            # Show some of the doc contents for debug
            for i, doc in enumerate(docs):
                print(f"[DOC {i+1}] {doc.page_content[:200]}...")

            # Optional: check if documents are truly relevant
            if not any(word in doc.page_content.lower() for doc in docs for word in user_input.lower().split()):
                print("[RAG] Docs found, but none match query meaningfully. Falling back to LLM.", llm.invoke(user_input).content)
                return llm.invoke(user_input).content

            try:
                response = rag_chain.invoke({"query": user_input})
                print("[RAG] Response:", response)
                return response["result"]
            except Exception as e:
                print("[ERROR] RAG generation failed:", str(e))
                return "⚠️ An error occurred while answering your question."

    else:
        print("[RAG] No relevant documents found. Falling back to LLM.")
        return llm.invoke(user_input).content
