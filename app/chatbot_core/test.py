from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain.schema import HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import SystemMessage
from typing import Sequence
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

import sys
sys.path.append(".")
from configs.config import Load_config
CONFIG = Load_config()

from models.models import Gemini_loader, Model_flan_t5_loader
CONFIG_MODEL = Gemini_loader()
CONFIG_FLAN_MODEL = Model_flan_t5_loader()

from app.tools.other_tools import *
from app.prompt.prompt_template import *

class DictState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def LLM_with_tools(llm, tools: list, prompt):
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent = agent, tools=tools, verbose=True)
    return agent_executor

agent = LLM_with_tools(CONFIG_MODEL.load_gemini(), tools=[add,calc],prompt=agent_prompt)  

def call_agent(state: DictState):   
    # invoke model
    query = state["messages"][0].content
    print(query)
    response = agent.invoke({"input": query}) # => dic: {"input","ouput"}
    # Update message history with response:
    return {"messages": [response["output"]]}


class LLM_agent:
    def __init__(self, user_infor, session_id):
        self.model_name = user_infor
        self.session_id = session_id
        self.llm = CONFIG_FLAN_MODEL.create_model()
        
        workflow = StateGraph(state_schema=DictState)
        workflow.add_edge(START, "model")
        workflow.add_node("model", call_agent)

        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)
        self.config = {"configurable": {"thread_id": session_id}}

        
    def run(self, query):

        input_dict = {
            "messages": [HumanMessage(query)],
        }

    # try:
        # output = self.app.invoke(input_dict, self.config)
        # response = output["messages"][-1].content # last message = last AI response
        
        # return agent.invoke({"input": query})["output"]
        return call_agent(input_dict)
        
    # except Exception as e:
    #     print(e)

if __name__ == "__main__":
    # rag = LLM_agent(user_infor="thao", session_id="1234")
    while (1):
        query = input("Enter your query: ")
        input_dict = {
            "messages": [HumanMessage(query)],
        }

        response = call_agent(input_dict)
        # response = rag.run(query)
        print(response)


