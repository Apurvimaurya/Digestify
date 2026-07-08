import numpy as np

#naive retriever

def naive_retriever(query, chunks, k):
    results=[]
    query_norm=np.linalg.norm(query)
    for chunk in chunks:
        chunk_norm = np.linalg.norm(chunk["embedding"])

        if query_norm == 0 or chunk_norm == 0:
            score = 0
        else:
            score = np.dot(query, chunk["embedding"]) / (
                query_norm * chunk_norm
            )
        results.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "page": chunk["page"],
                "score": score
            }
        )
    results.sort(key=lambda x: x.get("score",0), reverse=True)
    return results[:k]
        




