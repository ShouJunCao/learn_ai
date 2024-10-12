# 由于学生端与教师端环境的区别
# 对pysqlite的兼容处理
import os

from _01_file_split import extract_text_from_pdf
from _03_vector_search import get_embeddings

if os.environ.get('CUR_ENV_IS_STUDENT',False):
    import sys
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# 为了演示方便，我们只取两页（第一章）
paragraphs = extract_text_from_pdf(
    "llama2.pdf",
    page_numbers=[2, 3],
    min_line_length=10
)

import chromadb
from chromadb.config import Settings


class MyVectorDBConnector:
    def __init__(self, collection_name, embedding_fn):
        chroma_client = chromadb.Client(Settings(allow_reset=True))

        # 为了演示，实际不需要每次 reset()
        chroma_client.reset()

        # 创建一个 collection
        self.collection = chroma_client.get_or_create_collection(
            name=collection_name)
        self.embedding_fn = embedding_fn

    def add_documents(self, documents):
        '''向 collection 中添加文档与向量'''
        self.collection.add(
            embeddings=self.embedding_fn(documents),  # 每个文档的向量
            documents=documents,  # 文档的原文
            ids=[f"id{i}" for i in range(len(documents))]  # 每个文档的 id
        )

    def search(self, query, top_n):
        '''检索向量数据库'''
        results = self.collection.query(
            query_embeddings=self.embedding_fn([query]),
            n_results=top_n
        )
        return results

if __name__ == '__main__':
    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo", get_embeddings)
    # 向向量数据库中添加文档
    vector_db.add_documents(paragraphs)

    # user_query = "Llama 2有多少参数"
    user_query = "Does Llama 2 have a conversational variant"
    results = vector_db.search(user_query, 2)

    for para in results['documents'][0]:
        print(para + "\n")