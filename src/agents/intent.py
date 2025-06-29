from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

def get_intent_agent(llm):
    return create_react_agent(
        model=llm,
    tools=[],
    prompt=(
        "You are an intent agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with intent and emotions related tasks\n"
        "- You identify and classify the users input emotion and intent."
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="intent_agent",
)