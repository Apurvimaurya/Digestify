from embeddings import create_question_embeddings, create_chunk_embeddings, create_prompt_embeddings
from faiss_retriever import faiss_retriever
from pdfparser import extract_pdf_text
from langchain_chunker import langchain_chunker
from bm25_retriever import bm25_chunk_retriever
from retreiver import naive_retriever
from hybrid_retriever import hybrid_retriever
evaluation_set=[

    {
        "question":"What is Lossless Decompostion ?" ,
        "expected_chunks":[7]
    },
    {
        "question": "Example of Lossless Decomposition ?",
        "expected_chunks":[8]
    },
    {
        "question": "What are Functional Dependencies ?" ,
        "expected_chunks":[10]
    },
    {
        "question": "What is a Legal Instance of a Relation ?",
        "expected_chunks":[14]
    },
    {
        "question":"What is a Closure?" ,
        "expected_chunks":[16]
    },
    {
        "question": "What is superkey ?",
        "expected_chunks":[17]
    },
    {
        "question": "What is the use of Functional Dependencies",
        "expected_chunks": [14]
    },
    {
        "question": "What is a trivial FD ?",
        "expected_chunks":[15]
    },
    {
        "question": "What is Dependency Preservation ?",
        "expected_chunks":[25]
    },
    {
        "question": "What is BCNF?" ,
        "expected_chunks":[29,30,31]
    },
    {
        "question": "What is 3NF?",
        "expected_chunks": [35,36,37]
    },
    {
        "question": "Compare BCNF and 3NF",
        "expected_chunks":[40]
    },
    {
        "question": "What is a Closure of FD ?",
        "expected_chunks":[47,48]
    },
    {
        "question": "What are Armstrong's Axionms ?",
        "expected_chunks":[50]
    },
    {
        "question": "Procedure of computing closure ?",
        "expected_chunks":[51,52]
    },
    {
        "question": "What are the uses of Attribute Closure ?",
        "expected_chunks":[56,57]
    },
    {
        "question": "What is Cannonical cover ?",
        "expected_chunks":[58,59,69]
    },
    {
        "question": "What are extraneous attributes ?",
        "expected_chunks":[59,60,64,65]
    },
    {
        "question": "What is bcnf decompostion algo ?",
        "expected_chunks":[86]
    },
    {
        "question": "what is 3nf decompostion algorithm ?",
        "expected_chunks":[95,96,97]
    },
    
    
]
corpus, clean_pages = extract_pdf_text("notebooks/Normalization.pdf")
lc_chunks = langchain_chunker(clean_pages, 500, 100)
embed, vectormatrix= create_chunk_embeddings(lc_chunks)


def evaluate_faiss():
    success=0
    
    for q in evaluation_set:
        prompt_e= create_prompt_embeddings(q["question"])
        expected= set(q["expected_chunks"])
        retrieved= { chunk["chunk_id"] for chunk in faiss_retriever(prompt_e, embed, vectormatrix, 5)}
        if expected & retrieved:
            success+=1
    score= success/len(evaluation_set)
    return {"retriever":"faiss", "Precision@k": score}
    
    

def evaluate_bm25():
    success=0
    
    for q in evaluation_set:
        prompt= q["question"]
        expected= set(q["expected_chunks"])
        retrieved= {chunk["chunk_id"] for chunk in bm25_chunk_retriever(lc_chunks, prompt, 5)}
        if expected & retrieved:
            success+=1
    score= success/len(evaluation_set)
    return {"retriever":"BM25", "Precision@k": score}

def evaluate_naive():
    success=0
    
    for q in evaluation_set:
        prompt_e= create_prompt_embeddings(q["question"])
        expected= set(q["expected_chunks"])
        retrieved= {chunk["chunk_id"] for chunk in naive_retriever(prompt_e ,embed, 5)}
        if expected & retrieved:
            success+=1
    score= success/len(evaluation_set)
    return {"retriever":"Naive", "Precision@k": score}
    

def evaluate_hybrid():
    success=0
    
    for q in evaluation_set:
        prompt= q["question"]
        prompt_e= create_prompt_embeddings(q["question"])
        expected= set(q["expected_chunks"])
        retrieved= {chunk["chunk_id"] for chunk in hybrid_retriever(lc_chunks, prompt, 5, prompt_e, embed, vectormatrix)}
        if expected & retrieved:
            success+=1
    score= success/len(evaluation_set)
    return {"retriever":"Hybrid", "Precision@k": score}



#evalutation
results = [

evaluate_naive(),

evaluate_faiss(),

evaluate_bm25(),

evaluate_hybrid()

]

for result in results:

    print(result)