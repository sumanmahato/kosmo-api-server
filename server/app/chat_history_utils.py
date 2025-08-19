from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import HumanMessage, AIMessage

class ChatHistoryConversationSummaryBufferMemory(ConversationSummaryBufferMemory):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
  
  def save_context(self, inputs:dict, outputs:dict):
    """
      inputs: {content: str, **kwargs}
      outputs: {content:str, **kwargs}
    """
    input_content = inputs["content"]
    output_content = outputs["content"]
    inputs.pop("content")
    outputs.pop("content")

    user_message = HumanMessage(
      content=input_content,
      **inputs
    )

    ai_message = AIMessage(
      content=output_content,
      **outputs
    )
    self.chat_memory.add_user_message(user_message)
    self.chat_memory.add_ai_message(ai_message)