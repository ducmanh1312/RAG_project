
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, END
from langchain.schema.output_parser import StrOutputParser
from typing import Sequence
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langchain.schema.runnable import RunnablePassthrough
from IPython.display import Image, display
import json

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
tools = [add,calc,text_to_sql, search]


class LLM_agent:
    def __init__(self, user_infor, session_id):
        self.model_name = user_infor
        self.session_id = session_id

    def create_agent(self,llm_model,tools):
        agent = llm_model.bind_tools(tools)
        self.runable = agent_chatprompt | agent

        builder = StateGraph(state_schema=DictState)
        builder.add_edge(START, "chatbot")
        builder.add_node("chatbot", self.call_agent)
        tool_node = BasicToolNode(tools)
        builder.add_node("mytools", tool_node)
        builder.add_conditional_edges(
            "chatbot", self.route_tools, {"tools": "mytools", END: END}
        )
        builder.add_edge("mytools", "chatbot") # return to chatbot to decide next step

        memory = MemorySaver()
        self.graph = builder.compile(checkpointer=memory)
        self.config = {"configurable": {"thread_id": self.session_id }}

    def call_agent(self,state: DictState):  
        query = state["messages"][0].content
        response = self.runable.invoke({"human_input":query}) # input: list([Basemessage])
        return {"messages": [response]} # Update message history with response
    
    def route_tools(self, state: DictState):
        # get last message
        if isinstance(state, list): # if state is a list
            ai_message = state[-1]
        elif messages := state.get("messages", []): # if state is a dict
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0: #
            return "tools"
        return END
    
    def display(self):
        img = Image(self.graph.get_graph().draw_mermaid_png())
        display(img)
        with open("langgraph_architect.png", "wb") as f:
            f.write(img.data)
    
    def print_history(self):
        state = self.graph.get_state(self.config).values
        for message in state["messages"]:
            message.pretty_print()

    def run(self, query):
        input_dict = {
            "messages": [ HumanMessage(query)]
        }

        try:
            output = self.graph.invoke(input_dict,self.config)
            response = output["messages"][-1].content # last message = last AI response
            return response
            
        except Exception as e:
            print(e)

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_dict = {tool.name: tool for tool in tools} # dict of tools

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]  # get last message
        else:
            raise ValueError("No message found in input")
        
        outputs = []
        for tool in message.tool_calls: # list of tool agent decide to call.
            tool_result = self.tools_dict[tool["name"]].invoke(
                tool["args"] # variable send to tool
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool["name"],
                    tool_call_id=tool["id"],
                )
            )
        return {"messages": outputs}


# SystemMessage(AGENT_SYSTEM),

if __name__ == "__main__":
    rag = LLM_agent(user_infor="thao", session_id="1234")
    rag.create_agent(llm_model,tools)
    rag.display()
    # while (1):
    #     query = input("Enter your query: ")
    #     if query == "q": 
    #         break
    #     response = rag.run(query) 
    #     print(response)












