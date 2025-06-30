from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from langchain.memory.chat_message_histories import RedisChatMessageHistory

redis_url = "redis://localhost:6379/0"

def get_memory(session_id: str):
    chat_history = RedisChatMessageHistory(
        url=redis_url,
        session_id=session_id
    )
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=3,
        return_messages=True,
        chat_memory=chat_history
    )

@tool
def retrieve_memory(memory) -> str:
    """Retrieve relevant chat history/context from memory."""
    return memory.load_memory_variables({})["chat_history"]


def get_memory_agent(llm, session_id: str):
    memory = get_memory(session_id)
    tools = [retrieve_memory]
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
            "You are a memory agent. Retrieve and provide relevant chat history/context for the current conversation.\n"
            "Available tools: {tools}\n"
            "Tool names: {tool_names}\n"
            "{agent_scratchpad}"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    agent = create_react_agent(model=llm, tools=tools, prompt=prompt, name="memory_agent")
    return agent, memory
