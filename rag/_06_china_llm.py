import json
import requests
import os

from dotenv import load_dotenv, find_dotenv

from _01_file_split import extract_text_from_pdf
from _05_rag_bot import RAG_Bot
from _04_vector_db import MyVectorDBConnector


# 通过鉴权接口获取 access token


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": os.getenv('ERNIE_CLIENT_ID'),
        "client_secret": os.getenv('ERNIE_CLIENT_SECRET')
    }

    return str(requests.post(url, params=params).json().get("access_token"))

# 调用文心千帆 调用 BGE Embedding 接口


def get_embeddings_bge(prompts):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/bge_large_en?access_token=" + get_access_token()
    payload = json.dumps({
        "input": prompts
    })
    headers = {'Content-Type': 'application/json'}


    response = requests.request(
        "POST", url, headers=headers, data=payload).json()
    data = response["data"]
    return [x["embedding"] for x in data]


# 调用文心4.0对话接口
def get_completion_ernie(prompt):

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    headers = {'Content-Type': 'application/json'}

    response = requests.request(
        "POST", url, headers=headers, data=payload).json()

    return response["result"]

if __name__ == '__main__':
    # 为了演示方便，我们只取两页（第一章）
    paragraphs = extract_text_from_pdf(
        "llama2.pdf",
        page_numbers=[2, 3],
        min_line_length=10
    )

    # 创建一个向量数据库对象
    new_vector_db = MyVectorDBConnector(
        "demo_ernie",
        embedding_fn=get_embeddings_bge
    )
    # 向向量数据库中添加文档
    new_vector_db.add_documents(paragraphs)

    # 创建一个RAG机器人
    new_bot = RAG_Bot(
        new_vector_db,
        llm_api=get_completion_ernie
    )

    user_query = "how many parameters does llama 2 have?"

    response = new_bot.chat(user_query)

    print(response)