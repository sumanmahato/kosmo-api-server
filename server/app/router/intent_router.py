from app.agents.query_agent import get_query_agent
from app.models.ollama_wrapper import get_llm
from app.prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain
from app.controllers.query_controller import handle_query_to_api
from app.agents.query_processing_agent import get_query_processing_agent
from app.conversation_utils import build_history
import logging

logger = logging.getLogger(__name__)

llm = get_llm()
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def route_intent(user_input: str, memory=None, summary=None):
    # Build context history safely
    history = build_history(summary, memory)

    inputs = {
        "user_input": user_input,
        "history": history
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
    print(f"[INTENT] LLM classification response: '{classification}'")
    print(f"[HISTORY]: '{history}'")

    # Route based on classification
    if classification == "da_query":
        agent = get_query_processing_agent()
        return agent.run(inputs)

    # Fallback to base model with or without history
    if history:
        prompt_with_history = f"History:\n{history}\n\nUser input: {user_input}"
        logger.debug(f"[LLM Fallback] Using history:\n{prompt_with_history}")
        return llm.invoke(prompt_with_history).content

    return llm.invoke(user_input).content
