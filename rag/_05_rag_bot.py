from _01_file_split import extract_text_from_pdf
from _02_llm import get_completion, build_prompt
from _04_vector_db import MyVectorDBConnector
from _03_vector_search import get_embeddings

prompt_template = """
    你是一个问答机器人。
    你的任务是根据下述给定的已知信息回答用户问题。

    已知信息:
    {context}

    用户问：
    {query}

    如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。
    请不要输出已知信息中不包含的信息或答案。
    请用中文回答用户问题。
    """

class RAG_Bot:

    def __init__(self, vector_db, llm_api, n_results=2):
        self.vector_db = vector_db
        self.llm_api = llm_api
        self.n_results = n_results

    def build_prompt(prompt_template, **kwargs):
        '''将 Prompt 模板赋值'''
        inputs = {}
        for k, v in kwargs.items():
            if isinstance(v, list) and all(isinstance(elem, str) for elem in v):
                val = '\n\n'.join(v)
            else:
                val = v
            inputs[k] = val
        return prompt_template.format(**inputs)

    def chat(self, user_query):
        # 1. 检索
        search_results = self.vector_db.search(user_query, self.n_results)

        # 2. 构建 Prompt
        prompt = build_prompt(
            prompt_template, context=search_results['documents'][0], query=user_query)

        # 3. 调用 LLM
        response = self.llm_api(prompt)
        return response

if __name__ == '__main__':
    # 为了演示方便，我们只取两页（第一章）
    paragraphs = extract_text_from_pdf(
        "llama2.pdf",
        page_numbers=[2, 3],
        min_line_length=10
    )

    # 创建一个向量数据库对象
    vector_db = MyVectorDBConnector("demo", get_embeddings)
    # 向向量数据库中添加文档
    vector_db.add_documents(paragraphs)

    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db,
        llm_api=get_completion
    )

    user_query = "llama 2有多少参数?"

    response = bot.chat(user_query)

    print(response)
