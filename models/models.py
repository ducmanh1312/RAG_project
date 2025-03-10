import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings("ignore")

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoConfig, pipeline, BitsAndBytesConfig
from langchain_huggingface import HuggingFacePipeline
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import torch
from langchain_google_genai import ChatGoogleGenerativeAI
from groq import Groq
from langchain_groq import ChatGroq

import sys
sys.path.append(".")
from configs.config import Load_config
CONFIG = Load_config()

class Gemini_loader:
   def load_gemini(self):
      return ChatGoogleGenerativeAI(
         model= CONFIG.GOOGLE_MODEL,
         google_api_key= CONFIG.GOOGLE_API_KEY
   )

   def load_gemini_text(self):
      return ChatGoogleGenerativeAI(
         model= CONFIG.GOOGLE_TEXT_MODEL,
         google_api_key= CONFIG.GOOGLE_API_KEY
   )


class Groq_loader:
   def __init__(self):
      self.model_1 = CONFIG.GROQ_MODEL1
      self.model_2 = CONFIG.GROQ_MODEL2
      self.api_key = CONFIG.GROQ_API_KEY
      self.temperature = CONFIG.GROQ_TEMPERATURE
      self.max_tokens = CONFIG.GROQ_MAX_TOKENS
      self.client = ChatGroq(
         model_name = self.model_1,
         api_key = self.api_key)

   def create_model(self):
      return self.client
      

# def parse_groq_stream(stream):
#    for chunk in stream:
#       if chunk.choices[0].delta.content is not None:
#          yield chunk.choices[0].delta.content


class Flan_t5_loader:
   def __init__(self):
      model_name = CONFIG.FLAN_MODEL
      config = AutoConfig.from_pretrained(model_name)
      self.device = "gpu" if torch.cuda.is_available() else "cpu"
      self.tokenizer = AutoTokenizer.from_pretrained(model_name)

      # if CONFIG.FLAN_QUANTIZATION == "4bit":
      #    bnb_config = BitsAndBytesConfig(
      #       load_in_4bit=True,
      #       bnb_4bit_use_double_quant=True,
      #       bnb_4bit_quant_type="nf4",
      #       bnb_4bit_compute_dtype=torch.bfloat16,
      #    )
      # else:
      #    bnb_config = None
         
      pipe = pipeline(
         "text2text-generation",
         model= AutoModelForSeq2SeqLM.from_pretrained(model_name,config=config),
         tokenizer= self.tokenizer,
         max_length= CONFIG.FLAN_MAX_LENGTH,
         temperature= CONFIG.FLAN_TEMPERATURE,
         # quantization_config=bnb_config,
         device= self.device
      )
      
      self.model = HuggingFacePipeline(pipeline = pipe)

   def create_model(self):
      return self.model




if __name__ == "__main__":
   llm_loader = Groq_loader()
   llm = llm_loader.create_model()

   # Gọi model và in kết quả
   response = llm.invoke("What is the capital of France?")
   print(response)






