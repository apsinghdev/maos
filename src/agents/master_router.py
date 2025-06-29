from langchain_tavily import TavilySearch
from langchain_fireworks import ChatFireworks
from langchain_ollama import ChatOllama
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
import os 
import time
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_together import ChatTogether
load_dotenv()
from agents.search import get_search_agent
st = time.time()


llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    max_retries=2,
    api_key=os.getenv("TOGETHER_API_KEY")
)

search_agent = get_search_agent(llm)

llm2 = ChatOllama(
    model="llama3:8b"
)


def pretty_print_messages(msg_chunk):
    for msg in msg_chunk.get("messages", []):
        role = msg.get("role", "unknown")
        print(f"{role}: {msg['content']}")

intent_agent = create_react_agent(
    model=llm2,
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
instruction_agent = create_react_agent(
    model=llm2,
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

conversation_agent = create_react_agent(
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

supervisor = create_supervisor(
    model=llm,
    agents=[search_agent, intent_agent,instruction_agent,conversation_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a search agent. Assign search-related tasks to this agent\n"
        "- an intent agent. Assign intent and emotion detection and classification related tasks to this agent\n"
        "- an instruction_agent. Assign instructions related tasks to this agent and make sure it completes all instructions."
        "- a conversation_agent. Assign conversation flow realted tasks to this agent."
        " Give the final output answer by getting all the results from all agents"
        "Assign agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()

# 
