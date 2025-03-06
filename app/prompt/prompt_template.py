from .template import *
from langchain.prompts import PromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import SystemMessage


agent_prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad"],
    template=(
        "Bạn là một trợ lý thông minh khả năng tính toán và trò chuyện với người dùng và hãy trả lời bằng tiếng việt xưng là em.\n"
        "Nếu câu hỏi liên quan đến phép toán, hãy sử dụng các công cụ có sẵn và trả lời kết quả.\n"
        "Nêuế câu hỏi liên quan đến truy vấn cơ sở dữ liệu, hãy sử dụng tool text_to_sql"
        "Nếu đó là một câu hỏi thông thường, hãy trả lời như một trợ lý AI.\n\n"
        "Câu hỏi: {input}\n"
        "{agent_scratchpad}"
    )
)# => string

chitchat_chatprompt = ChatPromptTemplate.from_messages(     
[
    SystemMessage(CHITCHAT_SYSTEM),
    HumanMessagePromptTemplate.from_template(CHITCHAT_HUMAN_MESSAGE)
]) # => list([Basemessage])
