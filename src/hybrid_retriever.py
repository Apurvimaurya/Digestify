from bm25_retriever import bm25_chunk_retriever
from faiss_retriever import faiss_retriever
import numpy as np

def hybrid_retriever(chunks, query, k, query_embedding, chunks_embedding, vectormatrix):
    bm25_chunks= bm25_chunk_retriever(chunks,query,k)
    faiss_chunks= faiss_retriever(query_embedding, chunks_embedding, vectormatrix, k)
    rrf_scores={}
    for rank, f in enumerate(faiss_chunks, start=1):
        rrf_scores[f["chunk_id"]]= rrf_scores.get(f["chunk_id"],0)+ 1/(60+rank)
    for rank, d in enumerate(bm25_chunks, start=1):
        rrf_scores[d["chunk_id"]]= rrf_scores.get(d["chunk_id"],0)+ 1/(60+rank)
    chunk_map={}
    for chunk in bm25_chunks+ faiss_chunks:
        chunk_map[chunk["chunk_id"]]= chunk
    sorted_rrf= sorted(rrf_scores.items(), key=lambda x:x[1], reverse=True)
    topk=[]
    for chunkid, score in sorted_rrf:
        chunk = chunk_map[chunk_id].copy()
        chunk["rrf_score"] = score
        topk.append(chunk)
    return topk[:k]

        
    
    
    
    