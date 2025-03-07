
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain.schema import HumanMessage, AIMessage
from langchain.schema.output_parser import StrOutputParser
from typing import Sequence
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

import sys
sys.path.append(".")
from configs.config import Load_config
CONFIG = Load_config()

from models.models import Groq_loader
from app.tools.text_to_sql import text_to_sql
from app.tools.other_tools import *
from app.prompt.prompt_template import *

# input format of model
class DictState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

model_loader = Groq_loader()
llm_model = model_loader.create_model()
tools = [add,calc,text_to_sql]

def LLM_with_tools(llm, tools, prompt):
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent = agent, tools=tools,verbose=True)
    return agent_executor


class RAG:
    def __init__(self, user_infor, session_id):
        self.model_name = user_infor
        self.session_id = session_id
        self.llm = llm_model

        runnable = chitchat_chatprompt | self.llm

        def call_model(state: DictState):   
            # invoke model
            query = state["messages"][0].content
            response = runnable.invoke({"human_input": query}) 

            # return response to workflow => update history
            return {"messages": [response]}

    
        workflow = StateGraph(state_schema=DictState)
        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model)

        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)
        self.config = {"configurable": {"thread_id": session_id}}

        
    def run(self, query):

        input_dict = {
            "messages": [HumanMessage(query)],
        }
        try:
            output = self.app.invoke(input_dict, self.config)
            response = output["messages"][-1].content # last message = last AI response
            return response
        except Exception as e:
            print(e)


if __name__ == "__main__":
    rag = RAG(user_infor="thao", session_id="1234")
    while (1):
        query = input("Enter your query: ")
        if query == "q": 
            break
        response = rag.run(query)
        print(response)












