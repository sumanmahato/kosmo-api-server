from langchain_core.tools import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json

DEFAULT_PII_DEFINITIONS = [
    {"id": "1368"}, {"id": "1369"}, {"id": "1325"}, {"id": "1370"}, {"id": "1371"},
    {"id": "1349"}, {"id": "1372"}, {"id": "1357"}, {"id": "1373"}, {"id": "1374"},
    {"id": "1328"}, {"id": "1375"}, {"id": "1329"}, {"id": "1350"}, {"id": "1376"},
    {"id": "1377"}, {"id": "1378"}, {"id": "1379"}, {"id": "1380"}, {"id": "1381"},
    {"id": "1382"}, {"id": "1351"}, {"id": "1333"}, {"id": "1383"}, {"id": "1384"},
    {"id": "1334"}, {"id": "1385"}, {"id": "1386"}, {"id": "1387"}, {"id": "1388"},
    {"id": "1335"}, {"id": "1389"}, {"id": "1390"}, {"id": "1391"}, {"id": "1392"},
    {"id": "1393"}, {"id": "1346"}, {"id": "1394"}, {"id": "1395"}, {"id": "1396"},
    {"id": "1397"}, {"id": "1398"}, {"id": "1399"}, {"id": "1400"}, {"id": "1401"},
    {"id": "1402"}, {"id": "1403"}, {"id": "1404"}, {"id": "1405"}, {"id": "1406"},
    {"id": "1407"}, {"id": "1408"}, {"id": "1409"}, {"id": "1410"}, {"id": "1362"},
    {"id": "1361"}, {"id": "1363"}, {"id": "1364"}, {"id": "1355"}, {"id": "1411"},
    {"id": "1412"}, {"id": "1413"}, {"id": "1337"}, {"id": "1415"}, {"id": "1414"},
    {"id": "1416"}, {"id": "1417"}, {"id": "1418"}
]

WORKFLOW_PROMPT = PromptTemplate(
    input_variables=["user_input", "history"],
    template="""
You are a workflow configuration assistant. 
Extract the following information from the conversation so far, considering BOTH the past history and the latest user input. 
If a field was already provided in the history, keep that value unless the user overrides it in the latest input. 
If a field has never been provided, leave it empty.

Conversation history:
{history}

Latest user input:
{user_input}

Respond with ONLY a JSON object with these exact fields:

{{
  "workflowServiceClass": "string (PII, AMAZON_REKOGNITION, or other classification type, empty if not provided)",
  "tagKey": "string (what label/tag to apply, empty if not provided)",
  "displayName": "string (workflow name, empty if not provided)"
}}

Examples:
User: "create a workflow to tag all PII data"
Response: {{"workflowServiceClass": "PII", "tagKey": "", "displayName": ""}}

User: "add Project as the tag"
Response: {{"workflowServiceClass": "PII", "tagKey": "Project", "displayName": ""}}

User: "name it HR-Workflow"
Response: {{"workflowServiceClass": "PII", "tagKey": "Project", "displayName": "HR-Workflow"}}

Now extract based on the conversation and the latest input.
"""
)



def build_workflow_config(extracted_params: dict, workflow_message: str, isComplete: bool) -> dict:
    """Build the complete workflow configuration"""
    return {
        "content": workflow_message,
        "classifier": "workflow",
        "isConversationComplete": isComplete,
        "data": extracted_params        
    }

def validate_workflow_config(extracted_params: dict) -> tuple:
    required_fields = ["workflowServiceClass", "tagKey", "displayName"]
    missing_arr = []
    isComplete = True
    for field in required_fields:
        if not extracted_params.get(field):
            missing_arr.append(field)
            isComplete = False  
        else: 
            0

    return (missing_arr, isComplete)

def create_workflow_message(missing_arr: list) -> str:
    if not missing_arr:
        return "All required information is provided. Review the workflow details and create it."

    field_map = {
        "workflowServiceClass": "workflow action",
        "tagKey": "tag key",
        "displayName": "display name"
    }

    friendly_list = [f"<b>{field_map.get(field, field)}</b>" for field in missing_arr]

    if len(friendly_list) == 1:
        field_text = friendly_list[0]
        verb = "is"
    else:
        field_text = ", ".join(friendly_list[:-1]) + f", and {friendly_list[-1]}"
        verb = "are"

    workflow_message = (
        f"It looks like the {field_text} {verb} missing. "
        f"Please provide {'it' if len(friendly_list) == 1 else 'them'} to move forward."
    )

    return workflow_message





def workflow_pipeline(user_input: str, llm, query_id: str, summary, history) -> dict:
    """Extract workflow parameters using LLM and create workflow configuration"""
    
    chain = LLMChain(llm=llm, prompt=WORKFLOW_PROMPT)
    
    try:

        response = chain.run(user_input=user_input, history = history)
        print(f"[DEBUG] LLM response: {response}")
        
        try:
            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean.replace('```json', '').replace('```', '').strip()
            elif response_clean.startswith('```'):
                response_clean = response_clean.replace('```', '').strip()
            
            extracted_params = json.loads(response_clean)
            print(f"[DEBUG] Extracted params: {extracted_params}")
            
            missing_arr, isComplete = validate_workflow_config(extracted_params)
            workflow_message = create_workflow_message(missing_arr)
            workflow_config = build_workflow_config(extracted_params, workflow_message, isComplete)
            
            return workflow_config
            
        except json.JSONDecodeError as e:
            print(f"[DEBUG] JSON parse error: {e}")
            print(f"[DEBUG] Raw response: {response}")
            
            # Fallback to defaults if JSON parsing fails
            default_params = {
                "workflowServiceClass": "PII",
                "tagKey": "Project",
                "displayName": "PII-ai-demo"
            }
            workflow_config = build_workflow_config(default_params, query_id)
            return workflow_config
            
    except Exception as e:
        return f"Error creating workflow: {str(e)}"

workflow_tool = Tool(
    name="WorkflowProcessor",
    func=workflow_pipeline,
    description=(
        "Use this to create workflow configurations from natural language input. "
        "This tool uses LLM to extract parameters and creates PII tagging workflows."
    ),
)