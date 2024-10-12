import json
from pydantic.v1 import BaseModel

def show_json(data):
    """用于展示json数据"""
    if isinstance(data, str):
        obj = json.loads(data)
        print(json.dumps(obj, indent=4, ensure_ascii=False))
    elif isinstance(data, dict) or isinstance(data, list):
        print(json.dumps(data, indent=4, ensure_ascii=False))
    elif issubclass(type(data), BaseModel):
        print(json.dumps(data.dict(), indent=4, ensure_ascii=False))

def show_list_obj(data):
    """用于展示一组对象"""
    if isinstance(data, list):
        for item in data:
            show_json(item)
    else:
        raise ValueError("Input is not a list")

from llama_index.core import SimpleDirectoryReader

reader = SimpleDirectoryReader(
        input_dir="./data", # 目标目录
        recursive=False, # 是否递归遍历子目录
        required_exts=[".pdf"] # (可选)只读取指定后缀的文件
    )
documents = reader.load_data()

if __name__ == "__main__":
    print(documents[0].text)
    show_json(documents[0].json())
