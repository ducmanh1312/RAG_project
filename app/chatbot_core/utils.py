from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain.schema import HumanMessage

import sys
sys.path.append(".")
from configs.config import Load_config
CONFIG = Load_config()

from models.models import Gemini_loader
CONFIG_MODEL = Gemini_loader()



        
    

        




