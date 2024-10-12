from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
# 加载 .env 文件中定义的环境变量
_ = load_dotenv(find_dotenv())

# 初始化 OpenAI 客户端
client = OpenAI()  # 默认使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL

# 消息
messages = [
    {
        "role": "system",
        "content": "你是AI助手小瓜，是 AGIClass.ai 的助教。这门课每周二、四上课。"  # 注入新知识
    },
    {
        "role": "user",
        "content": "帮我生成一个笑话？"  # 问问题。可以改改试试
    },

]

# 调用 GPT-4o-mini 模型
chat_completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

# 输出回复
print(chat_completion.choices[0].message.content)
print(chat_completion.choices[0].message.role)
print(chat_completion.choices[0].message.function_call)
print(chat_completion.choices[0].message.refusal)