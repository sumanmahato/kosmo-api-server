from app.agents.query_agent import get_query_agent
from app.models.ollama_wrapper import get_llm
from app.prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain
from app.agents.rag_agent import get_answer  # Centralized RAG logic

llm = get_llm()
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def _classify_intent(user_input: str) -> str:
    """
    Classifies input as 'da_query' or 'rag_query'.
    """
    try: 
        result = intent_chain.invoke({"user_input": user_input})
        classification = result.get("text", "").strip().lower()
        print(f"[INFO] Intent classification result: {classification}")
        if classification not in ["da_query", "rag_query"]:
            return "rag_query"  # fallback if LLM response is invalid
        return classification
    except Exception as e:
        print(f"[ERROR] Intent classification failed: {e}")
        return "rag_query"

def route_intent(user_input: str) -> str:
    try:
        # Step 1: Classify the intent
        classification = _classify_intent(user_input)

        # Step 2: Handle DA query
        if classification == "da_query":
            print("[Router] Detected DA Query.")
            agent = get_query_agent()
            return agent.run(user_input)

        # Step 3: Fallback to RAG-based answer
        rag_result = get_answer(user_input)
        if rag_result['answer']:
            print("[Router] Using RAG pipeline.")
            print(f"[RAG] Answer: {rag_result['answer']}")
            print(f"[RAG] Sources: {rag_result['sources']}")
            return rag_result['answer']

        # Step 4: Final fallback to LLM
        print("[Router] Fallback to LLM.")
        return llm.invoke(user_input).content

    except Exception as e:
        print(f"[ERROR] route_intent failed: {e}")
        return "⚠️ Error processing your query."
