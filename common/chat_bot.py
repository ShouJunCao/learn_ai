from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
# 加载 .env 文件中定义的环境变量
_ = load_dotenv(find_dotenv())

# 初始化 OpenAI 客户端
client = OpenAI()  # 默认使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL

messages = [
    {
        "role": "system",
        "content": "你是AI助手小瓜，是 AGIClass.ai 的助教。这门课每周二、四上课。"
    }
]

def chat_bot_response(user_input):
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    ai_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_response})
    
    return ai_response

# ... 删除之前的主循环代码 ...