from langchain_core.output_parsers import PydanticOutputParser

from langchain._09_pydantic import Date, prompt, query, llm

parser = PydanticOutputParser(pydantic_object=Date)

input_prompt = prompt.format_prompt(query=query)
output = llm.invoke(input_prompt)
if __name__ == '__main__':
    print("原始输出:\n" + output.content)

    print("\n解析后:")
    parser.invoke(output)