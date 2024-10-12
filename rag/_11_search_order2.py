from sentence_transformers import CrossEncoder

from rag._01_file_split import paragraphs
from rag._02_llm import get_completion
from rag._03_vector_search import get_embeddings
from rag._04_vector_db import MyVectorDBConnector
from rag._05_rag_bot import RAG_Bot
from rag._09_split_ana2 import split_text

if __name__ == '__main__':

    chunks = split_text(paragraphs, 300, 100)
    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo_text_split", get_embeddings)
    # 向向量数据库中添加文档
    vector_db.add_documents(chunks)
    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db,
        llm_api=get_completion
    )
    # model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512) # 英文，模型较小
    model = CrossEncoder('BAAI/bge-reranker-large', max_length=512)  # 多语言，国产，模型较大

    user_query = "how safe is llama 2"

    search_results = vector_db.search(user_query, 5)

    # user_query = "llama 2安全性如何"
    scores = model.predict([(user_query, doc)
                            for doc in search_results['documents'][0]])
    # 按得分排序
    sorted_list = sorted(
        zip(scores, search_results['documents'][0]), key=lambda x: x[0], reverse=True)
    for score, doc in sorted_list:
        print(f"{score}\t{doc}\n")