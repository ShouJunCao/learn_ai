from openai import OpenAI


client = OpenAI(
    api_key = "sk-P7ZmtDdeD4yw1gKiMmaNs9IlyhbyN5hAEaFhrqEiR9cczVMT",
    base_url = "https://api.fe8.cn/v1"
)

def get_completion(prompt, response_format="text", model="gpt-4o-mini"):
    messages = [{"role":"user", "content":prompt}]
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = 0,
        response_format = {"type":response_format},
    )
    return response.choices[0].message.content

# 基于 prompt 生成文本
# # 默认使用 gpt-4o-mini 模型
# def get_completion(prompt, response_format="text", model="gpt-4o-mini"):
#     messages = [{"role": "user", "content": prompt}]    # 将 prompt 作为用户输入
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=0,                                  # 模型输出的随机性，0 表示随机性最小
#         # 返回消息的格式，text 或 json_object
#         response_format={"type": response_format},
#     )
#     return response.choices[0].message.content          # 返回模型生成的文本

#任务描述
# instruction = """
# 你的任务是识别用户对手机流量套餐产品的选择条件。
# 每种流量套餐产品包含三个属性：名称，月费价格，月流量。
# 根据用户输入，识别用户在上述三种属性上的需求是什么。
# """
instruction = """
你的任务是识别用户对手机流量套餐产品的选择条件。
每种流量套餐产品包含三个属性：名称(name)，月费价格(price)，月流量(data)。
根据用户输入，识别用户在上述三种属性上的需求是什么。
"""

#用户输入
# input_text = """
# 办个500G的套餐。价格不超过200元
# """
# input_text = "办个100G以上的套餐"
# input_text = "有没有土豪套餐"

input_text = "那个便宜"

# 多轮对话上下文
context = f"""
客服：有什么可以帮您
用户：有什么100G以上的套餐推荐
客服：我们有畅游套餐和无限套餐，您有什么价格倾向吗
用户：{input_text}
"""
#输出格式
# output_format = """
# 以JSON格式输出
# """
output_format = """
以JSON格式输出。
1. name字段的取值为string类型，取值必须为以下之一：经济套餐、畅游套餐、无限套餐、校园套餐 或 null；

2. price字段的取值为一个结构体 或 null，包含两个字段：
(1) operator, string类型，取值范围：'<='（小于等于）, '>=' (大于等于), '=='（等于）
(2) value, int类型

3. data字段的取值为取值为一个结构体 或 null，包含两个字段：
(1) operator, string类型，取值范围：'<='（小于等于）, '>=' (大于等于), '=='（等于）
(2) value, int类型或string类型，string类型只能是'无上限'

4. 用户的意图可以包含按price或data排序，以sort字段标识，取值为一个结构体：
(1) 结构体中以"ordering"="descend"表示按降序排序，以"value"字段存储待排序的字段
(2) 结构体中以"ordering"="ascend"表示按升序排序，以"value"字段存储待排序的字段

输出中只包含用户提及的字段，不要猜测任何用户未直接提及的字段，不输出值为null的字段。
"""

# example = """
# 便宜的套餐：{"sort":{"ordering"="ascend","value"="price"}}
# 有没有不限流量的：{"data":{"operator":"==","value":"无上限"}}
# 流量大的：{"sort":{"ordering"="descend","value"="data"}}
# 100G以上流量的套餐最便宜的是哪个：{"sort":{"ordering"="ascend","value"="price"},"data":{"operator":">=","value":100}}
# 月费不超过200的：{"price":{"operator":"<=","value":200}}
# 就要月费180那个套餐：{"price":{"operator":"==","value":180}}
# 经济套餐：{"name":"经济套餐"}
# 土豪套餐：{"name":"无限套餐"}
# """

# 多轮对话的例子
example = """
客服：有什么可以帮您
用户：100G套餐有什么

{"data":{"operator":">=","value":100}}

客服：有什么可以帮您
用户：100G套餐有什么
客服：我们现在有无限套餐，不限流量，月费300元
用户：太贵了，有200元以内的不

{"data":{"operator":">=","value":100},"price":{"operator":"<=","value":200}}

客服：有什么可以帮您
用户：便宜的套餐有什么
客服：我们现在有经济套餐，每月50元，10G流量
用户：100G以上的有什么

{"data":{"operator":">=","value":100},"sort":{"ordering"="ascend","value"="price"}}

客服：有什么可以帮您
用户：100G以上的套餐有什么
客服：我们现在有畅游套餐，流量100G，月费180元
用户：流量最多的呢

{"sort":{"ordering"="descend","value"="data"},"data":{"operator":">=","value":100}}
"""

promopt = f"""
#目标
{instruction}

#输出格式
{output_format}

#示例
{example}

#多轮对话上下文
{context}
"""

print(f"Promopt:\n{promopt}")

response = get_completion(promopt, response_format="json_object")
print(f"Response:\n{response}")

