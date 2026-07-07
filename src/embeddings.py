from sentence_transformers import SentenceTransformer
model= SentenceTransformer('all-MiniLM-L6-v2')
def create_chunk_embeddings(chunks):
    embeddings=[]
    texts = [chunk["text"] for chunk in chunks]
    vectors = model.encode(texts)
    for chunk, vector in zip(chunks,vectors):
        embeddings.append({
            "chunk_id": chunk["chunk_id"],
            "embedding": vector,
            "source": chunk["source"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding_model": "all-MiniLM-L6-v2"
        })
    return embeddings, vectors

def create_prompt_embeddings(prompt):
    prompt_embedding= model.encode(prompt)
    return prompt_embedding

