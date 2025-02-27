import os
import time
import json
from chinese_utils import to_keywords

from elasticsearch7 import Elasticsearch, helpers
 # 使用中文的关键字提取函数
from nltk.corpus.reader import documents


class MyEsConnector:
    def __init__(self, es_client, index_name, keyword_fn):
        self.es_client = es_client
        self.index_name = index_name
        self.keyword_fn = keyword_fn

    def add_documents(self, documents):
        '''文档灌库'''
        if self.es_client.indices.exists(index=self.index_name):
            self.es_client.indices.delete(index=self.index_name)
        self.es_client.indices.create(index=self.index_name)
        actions = [
            {
                "_index": self.index_name,
                "_source": {
                    "keywords": self.keyword_fn(doc),
                    "text": doc,
                    "id": f"doc_{i}"
                }
            }
            for i, doc in enumerate(documents)
        ]
        helpers.bulk(self.es_client, actions)
        time.sleep(1)

    def search(self, query_string, top_n=3):
        '''检索'''
        search_query = {
            "match": {
                "keywords": self.keyword_fn(query_string)
            }
        }
        res = self.es_client.search(
            index=self.index_name, query=search_query, size=top_n)
        return {
            hit["_source"]["id"]: {
                "text": hit["_source"]["text"],
                "rank": i,
            }
            for i, hit in enumerate(res["hits"]["hits"])
        }
    
if __name__ == '__main__':

    # 引入配置文件
    ELASTICSEARCH_BASE_URL = os.getenv('ELASTICSEARCH_BASE_URL')
    ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')
    ELASTICSEARCH_NAME = os.getenv('ELASTICSEARCH_NAME')

    es = Elasticsearch(
        hosts=[ELASTICSEARCH_BASE_URL],  # 服务地址与端口
        http_auth=(ELASTICSEARCH_NAME, ELASTICSEARCH_PASSWORD),  # 用户名，密码
    )

    # 创建 ES 连接器
    es_connector = MyEsConnector(es, "demo_es_rrf", to_keywords)

    # 文档灌库
    es_connector.add_documents(documents)

    # 关键字检索
    keyword_search_results = es_connector.search(query, 3)

    print(json.dumps(keyword_search_results, indent=4, ensure_ascii=False))