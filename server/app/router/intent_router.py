from agents.query_agent import get_query_agent
from models.ollama_wrapper import get_llm
from prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain
from controllers.query_controller import handle_query_to_api

llm = get_llm()
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def route_intent(user_input: str):
    classification = intent_chain.run({"user_input": user_input}).strip().lower()
    print(f"[DEBUG] LLM classification response: {classification}")

    if "da_query" in classification:
        return get_query_agent()
    else:
        raise ValueError("Unsupported intent. Currently, only 'query' actions are supported.")


# def route_intent(user_input: str):
#     intent = classify_intent(user_input) 
#     if intent == "query":
#         return handle_query_to_api(user_input)
#     else:
#         raise ValueError("Unsupported intent.")
