from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

def get_search_agent(llm):
    web_search = TavilySearch(max_results=5)
    return create_react_agent(
        model=llm,
        tools=[web_search],
        prompt=(
            "You are a search agent.\n\n"
            "INSTRUCTIONS:\n"
            "- Assist ONLY with search-related tasks, DO NOT do anything else\n"
            "- After you're done with your tasks, respond to the supervisor directly\n"
            "- Respond ONLY with the results of your work, do NOT include ANY other text."
        ),
        name="search_agent",
    )