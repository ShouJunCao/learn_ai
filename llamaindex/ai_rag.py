from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.readers.file import PyMuPDFReader
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.retrievers import QueryFusionRetriever
# from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import time
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

EMBEDDING_DIM = 512
COLLECTION_NAME = "full_demo"
PATH = "./qdrant_db"

# 创建 Qdrant 向量数据库，并持久化到本地
client = QdrantClient(path=PATH)

# 指定全局llm与embedding模型
Settings.llm = OpenAI(temperature=0, model="gpt-4o")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=EMBEDDING_DIM)

splitter = SentenceSplitter(chunk_size=300, chunk_overlap=100)

# 加载 pdf 文档
documents = SimpleDirectoryReader("./data", file_extractor={".pdf": PyMuPDFReader()}).load_data()

# 切分nodes
nodes = splitter.get_nodes_from_documents(documents)

if client.collection_exists(collection_name=COLLECTION_NAME):
    client.delete_collection(collection_name=COLLECTION_NAME)

# 新建 collection
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
)

# 创建 Vector Store
vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME)

# 指定 Vector Store 用于 index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(
    nodes, storage_context=storage_context
)

# 使用混合检索
# bm25_retriever = BM25Retriever.from_defaults(nodes=nodes)

# 检索后排序模型 因无法成功安装sentence-transformers，故暂时未使用
# reranker = SentenceTransformerRerank(
#     model="BAAI/bge-reranker-large", top_n=2
# )

# RAG Fusion
fusion_retriever = QueryFusionRetriever(
    [
        index.as_retriever(),
        # bm25_retriever # 使用混合检索
    ],
    similarity_top_k=5,
    num_queries=3,  # 生成 query 数
    use_async=False,
    # query_gen_prompt="...",  # 可以自定义 query 生成的 prompt 模板
)

# 构建单轮 query engine
query_engine = RetrieverQueryEngine.from_args(
    fusion_retriever
   # ,node_postprocessors=[reranker]
)

# 对话引擎
chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine,
    # condense_question_prompt=... # 可以自定义 chat message prompt 模板
)

while True:
    question=input("User:")
    if question.strip() == "":
        break
    response = chat_engine.chat(question)
    print(f"AI: {response}")
