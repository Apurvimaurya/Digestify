import faiss
import numpy as np

def faiss_retriever(query_embedding, chunks_embedding, vectormatrix, k):
    query_embedding = query_embedding.reshape(1, -1)

    query_embedding= query_embedding.astype('float32')
    vectormatrix= vectormatrix.astype('float32')
    features= vectormatrix.shape[1]

    index= faiss.IndexFlatL2(features)
    index.add(vectormatrix)
    
    dist, ids= index.search(query_embedding, k)
    desired_chunks=[]
    for idx, distance in zip(ids[0], dist[0]):
        chunk = chunks_embedding[idx].copy()
        chunk["distance"] = float(distance)
        desired_chunks.append(chunk)
    
    return desired_chunks