from llama_index.readers.feishu_docs import FeishuDocsReader

# 见说明文档
app_id = "cli_a6f1c0fa1fd9d00b"
app_secret = "dMXCTy8DGaty2xn8I858ZbFDFvcqgiep"

# https://agiclass.feishu.cn/docx/FULadzkWmovlfkxSgLPcE4oWnPf
# 链接最后的 "FULadzkWmovlfkxSgLPcE4oWnPf" 为文档 ID
doc_ids = ["FULadzkWmovlfkxSgLPcE4oWnPf"]

# 定义飞书文档加载器
loader = FeishuDocsReader(app_id, app_secret)

# 加载文档
documents = loader.load_data(document_ids=doc_ids)


if __name__ == "__main__":
    # 显示前1000字符
    print(documents[0].text[:1000])
