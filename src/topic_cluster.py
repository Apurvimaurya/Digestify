from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque
model= SentenceTransformer('all-MiniLM-L6-v2')


def deduplication(questions,  threshold, chat_history):
    question_vectors = model.encode(questions)
    similarity_matrix= cosine_similarity(question_vectors)
    t_id=1;
    visited=set()
    clusters=[]
    for i in range(len(questions)):
        if i in visited:
            continue
        queue = deque([i])
        visited.add(i)
        cluster=[]

        while queue:
            front= queue.popleft()
            cluster.append(chat_history[front])
            for j in range(len(questions)):
                if j not in visited and similarity_matrix[front][j]>=threshold:
                    queue.append(j)
                    visited.add(j)
        clusters.append({
            "Topic_id": t_id,
            "Conversations": cluster
        })
        t_id+=1;


    return clusters