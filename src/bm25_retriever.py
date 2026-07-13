from rank_bm25 import BM25Okapi
import numpy as np
import re
def preprocess_bm25(text):
    
    text = re.sub(r"[^\w\s]", " ", text)   # remove punctuation
    text = " ".join(text.split())          # remove extra spaces
    return text.split()

def bm25_chunk_retriever(chunks, query, k):
    tokenized_corpus = [
        preprocess_bm25(chunk["text"])
        for chunk in chunks
    ]
    bm25= BM25Okapi(tokenized_corpus)

    tokenized_q= preprocess_bm25(query)

    scores= bm25.get_scores(tokenized_q)

    results=[]
    for chunk, score in zip(chunks,scores):
        temp= chunk.copy()
        temp["score"]= score
        results.append(temp)
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:k]
    





