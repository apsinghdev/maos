from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

def get_conversation_agent(llm):
    return create_react_agent(
        model=llm,
    tools=[],
    prompt=(
        "You are an conversation agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with conversation flow determination decisions.\n"
        "- You tell the conversation flow and next steps to be taken"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="conversation_agent",
) 