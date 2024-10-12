from rag._03_vector_search import get_embeddings, cos_sim, l2

if __name__ == "__main__":
    model = "text-embedding-3-large"
    dimensions = 128

    query = "国际争端"

    # 且能支持跨语言
    # query = "global conflicts"

    documents = [
        "联合国就苏丹达尔富尔地区大规模暴力事件发出警告",
        "土耳其、芬兰、瑞典与北约代表将继续就瑞典“入约”问题进行谈判",
        "日本岐阜市陆上自卫队射击场内发生枪击事件 3人受伤",
        "国家游泳中心（水立方）：恢复游泳、嬉水乐园等水上项目运营",
        "我国首次在空间站开展舱外辐射生物学暴露实验",
    ]

    query_vec = get_embeddings([query], model=model, dimensions=dimensions)[0]
    doc_vecs = get_embeddings(documents, model=model, dimensions=dimensions)

    print("向量维度: {}".format(len(query_vec)))

    print()

    print("Query与Documents的余弦距离:")
    for vec in doc_vecs:
        print(cos_sim(query_vec, vec))

    print()

    print("Query与Documents的欧氏距离:")
    for vec in doc_vecs:
        print(l2(query_vec, vec))
