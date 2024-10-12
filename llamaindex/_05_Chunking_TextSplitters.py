from llama_index.core import Document
from llama_index.core.node_parser import TokenTextSplitter

from llamaindex._02_load_local_data import show_json
from llamaindex._04_data_connector_from_feishu import documents

node_parser = TokenTextSplitter(
    chunk_size=100,  # 每个 chunk 的最大长度
    chunk_overlap=50  # chunk 之间重叠长度
)

nodes = node_parser.get_nodes_from_documents(
    documents, show_progress=False
)

show_json(nodes[0].json())
show_json(nodes[1].json())