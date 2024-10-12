
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.readers.file import PyMuPDFReader

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 加载 pdf 文档
documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".pdf"],
    file_extractor={".pdf": PyMuPDFReader()}
).load_data()

# 定义 Node Parser
node_parser = TokenTextSplitter(chunk_size=300, chunk_overlap=100)

# 切分文档
nodes = node_parser.get_nodes_from_documents(documents)

# 构建 index
index = VectorStoreIndex(nodes)

# 获取 retriever
vector_retriever = index.as_retriever(
    similarity_top_k=2 # 返回2个结果
)

# 检索
results = vector_retriever.retrieve("Llama2有多少参数")
if __name__ == '__main__':
    print(results[0].text)
    print()
    print()
    print()
    print(results[1].text)