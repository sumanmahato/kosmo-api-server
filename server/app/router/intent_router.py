from app.models.ollama_wrapper import get_llm
from app.prompts.intent_prompt import intent_prompt
from langchain.chains import LLMChain
from app.agents.rag_agent import get_answer  # Centralized RAG logic
from app.agents.query_processing_agent import get_query_processing_agent
from app.agents.workflows_agent import get_workflow_processing_agent
from app.router.bert_router import BertIntentRouter
import logging

logger = logging.getLogger(__name__)

#normal intent router
# llm = get_llm()
# intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def route_intent(user_input: str, summary: str = "", history: list = None):
    if history is None:
        history = []
        
        
    inputs = {
        "user_input": user_input,
        "history": history,
        "summary": summary,
    }
    mock_summary = "The human asks the AI to find directory paths where the path contains 'img'. The AI provides a response with various filters and conditions for searching files, specifically focusing on directories containing 'img' in their names."
    mock_history = [
        {"role": "human", "content": "locate directory paths with substring img_1", "classifier": "da_query"},
        {"role": "ai", "content": "system response", "classifier": "da_query"},
        {"role": "human", "content": "create workflow for PII files and name it us-license", "classifier": "workflow"},
        {"role": "ai", "content": {"data": {"workflowServiceClass": "PII", "tagKey": "", "displayName": "us-license"}, "response": "tag key is missing, please provide it"}, "classifier": "workflow", "isConversationComplete": False}
    ]

    if len(history) != 0 and history[-1].get("isConversationComplete") is False:
        last_intent = history[-1].get("classifier")
        print(f"[Router] Incomplete {user_input} context, routing directly.")
        if last_intent == "workflow":
            agent = get_workflow_processing_agent()
            return agent.run(inputs, history, summary), "workflow"
        # fallback if no known last_intent
        return get_answer(user_input, history=history, summary=summary), "rag_query"


    print(f"[DEBUG] Inputs: {inputs}")

    # normal intent router
    # response = intent_chain.invoke(inputs)
    
    #bert
    bertRouter = BertIntentRouter()
    response = bertRouter.predict(user_input)

    if isinstance(response, dict) and "text" in response:
        classification = response["text"].strip().lower()
    else:
        classification = str(response).strip().lower()

    cleaned_classification = classification.strip('`"\'')
    print(f"[INTENT] LLM classification response: '{cleaned_classification}'")
    # cleaned_classification = "workflow"
    if cleaned_classification == "da_query":
        agent = get_query_processing_agent()
        return agent.run(inputs), "da_query"
    elif cleaned_classification == "workflow":
        agent = get_workflow_processing_agent()
        return agent.run(inputs, mock_history, mock_summary), "workflow"

    print("[Router] Falling back to RAG-based answer.")
    rag_result = get_answer(user_input, history=history, summary=summary)
    return rag_result, "rag_query"

