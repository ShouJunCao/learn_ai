from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from langchain._10_OutputParser import parser
from langchain._11_PydanticOutputParser import output

new_parser = PydanticOutputParser.from_llm(parser=parser, llm=ChatOpenAI())

bad_output = output.content.replace("4","四")
print("PydanticOutputParser:")
try:
    parser.invoke(bad_output)
except Exception as e:
    print(e)

print("OutputFixingParser:")
new_parser.invoke(bad_output)