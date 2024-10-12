from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

response = query_engine.query("llama2有多少参数")
print(response)