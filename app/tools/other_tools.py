from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.types import Command, interrupt

from typing import Annotated
import sys
sys.path.append(".")
import os
from configs.config import Load_config
CONFIG = Load_config()
os.environ['TAVILY_API_KEY'] = CONFIG.TAVILY_API_KEY

# Search tool
search = TavilySearchResults(max_results=2)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

@tool
def human_birthday(name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    """Request assistance from a human about birthday information"""
    human_response = interrupt({    # pause graph execution and surface value below to human
        "question": "Is it correct?", 
        "name": name, 
        "birthday": birthday
        }) 
    
    if human_response.get("correct").lower().startswith("y"):
        verified_name = name
        verified_birthday = birthday
        response = "correct"
    else: 
        verified_name =human_response.get("name", name)
        verified_birthday = human_response.get("birthday", birthday)
        response = f"Made a correction: {human_response}"

    state_update = {
        "name": verified_name,
        "birthday": verified_birthday,
        "response": [ToolMessage(content=response, tool_call_id=tool_call_id)]
    }
    return Command(update=state_update)

    

    return human_response["data"]


@tool
def add(a: int, b: int) -> int:
    """Adds two numbers """
    return a + b

@tool
def calc(a: int, b: int) -> int:
    """Tính theo công thức đặc biệt"""
    return a*a + b*b






