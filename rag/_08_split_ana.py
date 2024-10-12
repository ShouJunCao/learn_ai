from rag._01_file_split import paragraphs
from rag._02_llm import get_completion
from rag._03_vector_search import get_embeddings
from rag._04_vector_db import MyVectorDBConnector
from rag._05_rag_bot import RAG_Bot

if __name__ == '__main__':
    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo_text_split", get_embeddings)
    # 向向量数据库中添加文档
    vector_db.add_documents(paragraphs)

    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db,
        llm_api=get_completion
    )

    # user_query = "llama 2有商用许可协议吗"
    user_query = "llama 2 chat有多少参数"
    search_results = vector_db.search(user_query, 2)

    for doc in search_results['documents'][0]:
        print(doc + "\n")

    print("====回复====")
    response = bot.chat(user_query)
    print(response)