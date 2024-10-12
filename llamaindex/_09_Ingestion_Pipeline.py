import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.interval = self.end - self.start
        print(f"耗时 {self.interval*1000} ms")

from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, SimpleDirectoryReader

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import VectorStoreIndex
from llama_index.readers.file import PyMuPDFReader
import nest_asyncio

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

nest_asyncio.apply() # 只在Jupyter笔记环境中需要此操作，否则会报错

client = QdrantClient(location=":memory:")
collection_name = "ingestion_demo"

collection = client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# 创建 Vector Store
vector_store = QdrantVectorStore(client=client, collection_name=collection_name)

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=300, chunk_overlap=100), # 按句子切分
        TitleExtractor(), # 利用 LLM 对文本生成标题
        OpenAIEmbedding(), # 将文本向量化
    ],
    vector_store=vector_store,
)

documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".pdf"],
    file_extractor={".pdf": PyMuPDFReader()}
).load_data()

# 计时
with Timer():
    # Ingest directly into a vector db
    pipeline.run(documents=documents)

# 创建索引
index = VectorStoreIndex.from_vector_store(vector_store)

# 获取 retriever
vector_retriever = index.as_retriever(similarity_top_k=1)

# 检索
results = vector_retriever.retrieve("Llama2有多少参数")

if __name__ == "__main__":
    print(results[0])
    pipeline.persist("./pipeline_storage")
    new_pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=300, chunk_overlap=100),
            TitleExtractor(),
        ],
    )

    # 加载缓存
    new_pipeline.load("./pipeline_storage")

    with Timer():
        nodes = new_pipeline.run(documents=documents)

    # 获取 retriever
    vector_retriever = index.as_retriever(similarity_top_k=5)

    # 检索
    nodes = vector_retriever.retrieve("Llama2 有商用许可吗?")

    for i, node in enumerate(nodes):
        print(f"[{i}] {node.text}\n")