from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from llamaindex._07_SimpleVectorStore import nodes

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = QdrantClient(location=":memory:")
collection_name = "demo"
collection = client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
# storage: 指定存储空间
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 创建 index：通过 Storage Context 关联到自定义的 Vector Store
index = VectorStoreIndex(nodes, storage_context=storage_context)

# 获取 retriever
vector_retriever = index.as_retriever(similarity_top_k=2)

# 检索
results = vector_retriever.retrieve("Llama2有多少参数")

if __name__ == '__main__':
    print(results[0])
    print(results[1])