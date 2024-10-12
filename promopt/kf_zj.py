from openai import OpenAI
client = OpenAI(
    api_key = "sk-P7ZmtDdeD4yw1gKiMmaNs9IlyhbyN5hAEaFhrqEiR9cczVMT",
    base_url = "https://api.fe8.cn/v1"
)


def get_completion(prompt, model="gpt-4o-mini"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


instruction = """
给定一段用户与手机流量套餐客服的对话，。
你的任务是判断客服的回答是否符合下面的规范：

- 必须有礼貌
- 必须用官方口吻，不能使用网络用语
- 介绍套餐时，必须准确提及产品名称、月费价格和月流量总量。上述信息缺失一项或多项，或信息与事实不符，都算信息不准确
- 不可以是话题终结者

已知产品包括：

经济套餐：月费50元，月流量10G
畅游套餐：月费180元，月流量100G
无限套餐：月费300元，月流量1000G
校园套餐：月费150元，月流量200G，限在校学生办理
"""

# 输出描述
output_format = """
如果符合规范，输出：Y
如果不符合规范，输出：N
"""

context = """
用户：你们有什么流量大的套餐
客服：亲，我们现在正在推广无限套餐，每月300元就可以享受1000G流量，您感兴趣吗？
"""

cot = ""
# cot = "请一步一步分析对话"

prompt = f"""
# 目标
{instruction}
{cot}

# 输出格式
{output_format}

# 对话上下文
{context}
"""

response = get_completion(prompt)
print(response)