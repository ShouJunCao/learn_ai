from langchain._01_ChatOpenAI import llm
from langchain_core.messages import (
        AIMessage,  # 等价于OpenAI接口中的assistant role
        HumanMessage,  # 等价于OpenAI接口中的user role
        SystemMessage  # 等价于OpenAI接口中的system role
    )

messages = [
    SystemMessage(content="你是AGIClass的课程助理。"),
    HumanMessage(content="我是学员，我叫王卓然。"),
    AIMessage(content="欢迎！"),
    HumanMessage(content="我是谁")
]

if __name__ == '__main__':
    ret = llm.invoke(messages)

    print(ret.content)