from langchain_openai import ChatOpenAI

from langchain._04_PromptTemplate import template

# 定义 LLM
llm = ChatOpenAI()
# 通过 Prompt 调用 LLM
ret = llm.invoke(template.format(subject='小明'))
if __name__ == '__main__':
    # 打印输出
    print(ret.content)