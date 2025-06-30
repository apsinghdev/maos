from langchain_tavily import TavilySearch
from langchain_fireworks import ChatFireworks
from langchain_ollama import ChatOllama
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
import os 
import time
from dotenv import load_dotenv
from langchain_together import ChatTogether
load_dotenv()
from agents.search import get_search_agent
from agents.intent import get_intent_agent
from agents.instruction import get_instruction_agent
from agents.conversation import get_conversation_agent
from agents.memory import get_memory_agent
st = time.time()


llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    max_retries=2,
    api_key=os.getenv("TOGETHER_API_KEY")
)

search_agent = get_search_agent(llm)
intent_agent = get_intent_agent(llm)
instruction_agent = get_instruction_agent(llm)
conversation_agent = get_conversation_agent(llm)
memory_agent, _ = get_memory_agent(llm, session_id="default-session")

llm2 = ChatOllama(
    model="llama3:8b"
)


def pretty_print_messages(msg_chunk):
    for msg in msg_chunk.get("messages", []):
        role = msg.get("role", "unknown")
        print(f"{role}: {msg['content']}")

supervisor = create_supervisor(
    model=llm,
    agents=[search_agent, intent_agent,instruction_agent,conversation_agent,memory_agent],
    prompt=(
        "You are a supervisor managing five agents:\n"
        "- a search agent. Assign search-related tasks to this agent\n"
        "- an intent agent. Assign intent and emotion detection and classification related tasks to this agent\n"
        "- an instruction_agent. Assign instructions related tasks to this agent and make sure it completes all instructions."
        "- a conversation_agent. Assign conversation flow realted tasks to this agent."
        "- a memory agent. Assign task to retrieve relevant chat history/context"
        " Give the final output answer by getting all the results from all agents"
        "Assign agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()
