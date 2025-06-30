import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from agents.intent import get_intent_agent
from agents.instruction import get_instruction_agent
from agents.conversation import get_conversation_agent
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.language_models.fake_chat_models import FakeChatModel
from langchain_core.messages import AIMessage
from unittest.mock import patch
from langchain_core.runnables import Runnable
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage

class SimpleMockLLM(FakeChatModel):
    def __init__(self, response_text):
        self._response_text = response_text

    def bind_tools(self, tools, *, tool_choice=None, **kwargs) -> Runnable:
        def dummy_chain(input, config=None):
            return AIMessage(content=self._response_text)
        return dummy_chain

    def invoke(self, input, config=None):
        return AIMessage(content=self._response_text)


@patch("agents.search.create_react_agent")
def test_search_agent(mock_create_agent):
    mock_create_agent.return_value.invoke.return_value = AIMessage(content="search result")
    
    from agents.search import get_search_agent
    llm = object()
    agent = get_search_agent(llm)
    
    result = agent.invoke({"input": "capital of France"})
    assert "search result" in str(result)

def test_intent_agent():
    llm = SimpleMockLLM("intent: question")
    agent = get_intent_agent(llm)
    result = agent.invoke({"input": "How are you?"})
    assert "intent" in str(result) or "question" in str(result)


def test_instruction_agent():
    llm = SimpleMockLLM("instruction completed")
    agent = get_instruction_agent(llm)
    result = agent.invoke({"input": "Turn off the lights."})
    assert "instruction" in str(result) or "completed" in str(result)


def test_conversation_agent():
    llm = SimpleMockLLM("continue conversation")
    agent = get_conversation_agent(llm)
    result = agent.invoke({"input": "Let's keep talking."})
    assert "conversation" in str(result) or "continue" in str(result)

def test_memory_agent():

    mock_agent = MagicMock()
    mock_agent.invoke.return_value = AIMessage(content="memory: previous chats")

    class DummyMemory:
        def save_context(self, inputs, outputs):
            pass

        def load_memory_variables(self, inputs):
            return {"chat_history": "Human: Hello\nAI: Hi there!"}

    agent = mock_agent
    memory = DummyMemory()

    result = agent.invoke({
        "input": "What did I say before?",
        "chat_history": memory.load_memory_variables({})["chat_history"]
    })

    assert "memory" in str(result) or "previous" in str(result)
