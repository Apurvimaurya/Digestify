from rank_bm25 import BM25Okapi
import numpy as np

def bm25_chunk_retriever(chunks, query, k):
    corpus= [chunk["text"] for chunk in chunks]
    tokenized_c= [c.split() for c in corpus]
    bm25= BM25Okapi(tokenized_c)
    tokenized_q= query.lower().split()
    scores= bm25.get_scores(tokenized_q)
    result=[]
    for chunk, score in zip(chunks,scores):
        r_chunk= chunk.copy()
        r_chunk["score"]= score
        result.append(r_chunk)
    desired_chunks = sorted(
    result,
    key=lambda x: x["score"],
    reverse=True
)
    return desired_chunks[:k]
    





