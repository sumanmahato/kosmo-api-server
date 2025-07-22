from app.agents.query_agent import get_query_agent
from app.models.ollama_wrapper import get_llm
from app.prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain
from app.agents.rag_agent import get_answer  # Centralized RAG logic

llm = get_llm()
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def _classify_intent(user_input: str) -> str:
    """
    Classifies input as 'da_query', 'rag_query', or 'unknown'.
    Cleans and normalizes the output.
    """
    try:
        result = intent_chain.invoke({"user_input": user_input})
        raw_classification = (
            result.get("text", "") if isinstance(result, dict) else str(result)
        ).strip().lower()

        print(f"[DEBUG] Raw classification output: {repr(raw_classification)}")

        # Normalize output to exact values
        if "da_query" in raw_classification:
            return "da_query"
        elif "rag_query" in raw_classification:
            return "rag_query"
        else:
            return "unknown"
    except Exception as e:
        print(f"[ERROR] Intent classification failed: {e}")
        return "unknown"

def route_intent(user_input: str) -> str:
    try:
        # Step 1: Check RAG results first
        rag_result = get_answer(user_input)
        if rag_result['answer']:
            print("[Router] RAG returned an answer, using RAG pipeline.")
            print(f"[RAG] Answer: {rag_result['answer']}")
            print(f"[RAG] Sources: {rag_result['sources']}")
            return rag_result['answer']

        # Step 2: If RAG doesn't return, check intent
        classification = _classify_intent(user_input)
        if classification == "da_query":
            print("[Router] Detected DA Query.")
            agent = get_query_agent()
            return agent.run(user_input)

        else:
            print("[Router] Fallback to LLM.")
            return llm.invoke(user_input).content

    except Exception as e:
        print(f"[ERROR] route_intent failed: {e}")
        return "⚠️ Error processing your query."

