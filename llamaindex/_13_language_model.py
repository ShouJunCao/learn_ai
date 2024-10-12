from llama_index.llms.openai import OpenAI

from llamaindex._11_PromptTemplate import prompt

from dotenv import load_dotenv, find_dotenv

from llamaindex._12_ChatPromptTemplate import text_qa_template

_ = load_dotenv(find_dotenv())

llm = OpenAI(temperature=0, model="gpt-4o")

response = llm.complete(prompt.format(topic="小明"))

print(response.text)
print('---------------------------------------')

response = llm.complete(
    text_qa_template.format(
        name="瓜瓜",
        context="这是一个测试",
        question="你是谁，我们在干嘛"
    )
)

print(response.text)

from llama_index.core import Settings

Settings.llm = OpenAI(temperature=0, model="gpt-4o")

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# 全局设定
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=512)

