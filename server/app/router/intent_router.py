from app.agents.query_agent import get_query_agent
from app.models.ollama_wrapper import get_llm
from app.prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain
from app.controllers.query_controller import handle_query_to_api
from app.agents.query_processing_agent import get_query_processing_agent

llm = get_llm()
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def route_intent(user_input: str):
    classification = intent_chain.run({"user_input": user_input}).strip().lower()
    print(f"[DEBUG] LLM classification response: {classification}")

    if "da_query" in classification:
        # agent = get_query_agent()
        # return agent.run(user_input)  # returns the response string

        agent = get_query_processing_agent()
        return agent.run(user_input)
    else:
        return llm.invoke(user_input).content


# def route_intent(user_input: str):
#     intent = classify_intent(user_input) 
#     if intent == "query":
#         return handle_query_to_api(user_input)
#     else:
#         raise ValueError("Unsupported intent.")
