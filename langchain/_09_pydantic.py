from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import _01_ChatOpenAI

# 定义你的输出对象
class Date(BaseModel):
    year: int = Field(description="Year")
    month: int = Field(description="Month")
    day: int = Field(description="Day")
    era: str = Field(description="BC or AD")



from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import PydanticOutputParser


model_name = 'gpt-4o-mini'
temperature = 0
llm = ChatOpenAI(model_name=model_name, temperature=temperature)

# 定义结构化输出的模型
structured_llm = llm.with_structured_output(Date)

template = """提取用户输入中的日期。
用户输入:
{query}"""

prompt = PromptTemplate(
    template=template,
)

query = "2023年四月6日天气晴..."
input_prompt = prompt.format_prompt(query=query)

if __name__ == '__main__':
    data = structured_llm.invoke(input_prompt)
    print(data)

json_schema = {
    "title": "Date",
    "description": "Formated date expression",
    "type": "object",
    "properties": {
        "year": {
            "type": "integer",
            "description": "year, YYYY",
        },
        "month": {
            "type": "integer",
            "description": "month, MM",
        },
        "day": {
            "type": "integer",
            "description": "day, DD",
        },
        "era": {
            "type": "string",
            "description": "BC or AD",
        },
    },
}
structured_llm = llm.with_structured_output(json_schema)

if __name__ == '__main__':
    data = structured_llm.invoke(input_prompt)
