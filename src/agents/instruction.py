from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

def get_instruction_agent(llm):
    return create_react_agent(
        model=llm,
    tools=[],
    prompt=(
        "You are an instructions agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with completing the instructions given by the user as input\n"
        "- You identify and classify the user given instructions and fulfil them."
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="instructions_agent",
)