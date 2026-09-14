from langchain_core.prompts import ChatPromptTemplate

def create_prompt():
  prompt = ChatPromptTemplate.from_messages([
    (
      "system",
      """You are a helpful DevOps assistant.
Answer the question using only the provided context.
If the answer is not present in the context,
then say like I'm sorry, I don't know or haven't found the information.

Do not make up information."""
        ),
  (
  "human",
  """
  Context: {context} 
  Question: {question}
  Conversation history: {conversation}
  """
        )
  ])
  return prompt


