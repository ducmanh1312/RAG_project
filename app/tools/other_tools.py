from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

import sys
sys.path.append(".")
import os
from configs.config import Load_config
CONFIG = Load_config()
os.environ['TAVILY_API_KEY'] = CONFIG.TAVILY_API_KEY

# Search tool
search = TavilySearchResults(max_results=2)

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers """
    return a + b

@tool
def calc(a: int, b: int) -> int:
    """Tính theo công thức đặc biệt"""
    return a*a + b*b






