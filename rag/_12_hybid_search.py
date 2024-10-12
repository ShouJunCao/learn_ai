from rag._03_vector_search import get_embeddings, cos_sim

if   __name__ == '__main__':
    # 背景说明：在医学中“小细胞肺癌”和“非小细胞肺癌”是两种不同的癌症

    query = "非小细胞肺癌的患者"

    documents = [
        "玛丽患有肺癌，癌细胞已转移",
        "刘某肺癌I期",
        "张某经诊断为非小细胞肺癌III期",
        "小细胞肺癌是肺癌的一种"
    ]

    query_vec = get_embeddings([query])[0]
    doc_vecs = get_embeddings(documents)

    print("Cosine distance:")
    for vec in doc_vecs:
        print(cos_sim(query_vec, vec))