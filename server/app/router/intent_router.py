from app.models.ollama_wrapper import get_llm
from app.prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain
from app.agents.rag_agent import get_answer  # Centralized RAG logic
from app.agents.query_processing_agent import get_query_processing_agent
import logging

logger = logging.getLogger(__name__)

llm = get_llm()
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def route_intent(user_input: str, summary: str = "", history: str = ""):
    # Build context history safely

    inputs = {
        "user_input": user_input,
        "history": history,
        "summary": summary,
    }
    print(f"[DEBUG] Inputs: {inputs} {summary}")

    # Run classification
    response = intent_chain.invoke(inputs)

    # Adjust based on actual structure of response
    if isinstance(response, dict) and "text" in response:
        classification = response["text"].strip().lower()
    else:
        classification = str(response).strip().lower()
        classification = intent_chain.invoke(inputs).strip().lower()


    # Route based on classification
    cleaned_classification = classification.strip('`"\'')
    print(f"[INTENT] LLM classification response: '{cleaned_classification}'")
    if cleaned_classification == "da_query":
        agent = get_query_processing_agent()
        return agent.run(inputs), cleaned_classification
    
    print("[Router] Falling back to RAG-based answer.")
    # Fallback to RAG-based answer
    rag_result = get_answer(user_input, history=history, summary=summary)
    # if rag_result.get("answer"):
    print(f"[RAG] Answer: {rag_result['answer']}")
    print(f"[RAG] Sources: {rag_result.get('sources')}")
    return rag_result, "rag_query"
