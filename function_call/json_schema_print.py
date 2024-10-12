from pydantic import BaseModel
from openai import OpenAI
client = OpenAI(
    api_key = "sk-P7ZmtDdeD4yw1gKiMmaNs9IlyhbyN5hAEaFhrqEiR9cczVMT",
    base_url = "https://api.fe8.cn/v1"
)


from db_call_function import print_json


# def print_json(data):
#     """
#     打印参数。如果参数是有结构的（如字典或列表），则以格式化的 JSON 形式打印；
#     否则，直接打印该值。
#     """
#     if hasattr(data, 'model_dump_json'):
#         data = json.loads(data.model_dump_json())
#
#     if (isinstance(data, (list))):
#         for item in data:
#             print_json(item)
#     elif (isinstance(data, (dict))):
#         print(json.dumps(
#             data,
#             indent=4,
#             ensure_ascii=False
#         ))
#     else:
#         print(data)


class CalendarEvent(BaseModel):
    name: str
    date: str
    address: str
    participants: list[str]

completion = client.beta.chat.completions.parse( # 使用 beta 接口
    model="gpt-4o-mini-2024-07-18",  # 必须是版本大于 gpt-4o-mini-2024-07-18 或 gpt-4o-2024-08-06 的模型
    messages=[
        {"role": "system", "content": "解析出事件信息。"},
        {"role": "user", "content": "一般在周一晚上，老师会在他的视频号邀请一名 AI 全栈工程师课程的学员连麦直播。"},
    ],
    response_format=CalendarEvent,
)
event = completion.choices[0].message.parsed
print_json(event)