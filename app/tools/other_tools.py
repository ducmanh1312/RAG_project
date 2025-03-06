from langchain.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Adds two numbers """
    return a + b

@tool
def calc(a: int, b: int) -> int:
    """Tính theo công thức đặc biệt"""
    return a*a + b*b





