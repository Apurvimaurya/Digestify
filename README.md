# DIGESTIFY 📚🤖

> AI-powered Study Assistant built from scratch using Retrieval-Augmented Generation (RAG).

Digestify allows users to upload PDF study material, ask questions about the content, retrieve the most relevant information using multiple retrieval strategies, and (coming soon) generate concise study notes from an entire learning session.

---

## Features (Completed)

- PDF text extraction pipeline
- Document preprocessing
- Custom chunking engine
- LangChain Recursive Character Text Splitter comparison
- SentenceTransformer embeddings
- Custom cosine similarity retriever
- FAISS vector search
- BM25 keyword search
- Hybrid Retrieval (FAISS + BM25 using Reciprocal Rank Fusion)
- Retrieval Evaluation Harness
- Streamlit Chat UI

---

## Project Pipeline

```
                PDF
                 │
                 ▼
          PDF Parser
                 │
                 ▼
      Text Cleaning Pipeline
                 │
                 ▼
        Document Chunking
                 │
                 ▼
        Sentence Embeddings
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
     BM25 Search     Dense Search
                          │
                     FAISS Index
         └───────┬────────┘
                 ▼
      Reciprocal Rank Fusion
                 ▼
       Top-K Relevant Chunks
                 ▼
        (LLM Generation - WIP)
```

---

# Tech Stack

### Language

- Python

### Frontend

- Streamlit

### NLP / Retrieval

- Sentence Transformers
- FAISS
- rank-bm25

### PDF Processing

- PyPDF

### Utilities

- NumPy
- Regex
- Collections

---

# Project Structure

```
Digestify/

│
├── app.py
│
├── src/
│   ├── pdfparser.py
│   ├── chunker.py
│   ├── langchain_chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── faiss_retriever.py
│   ├── bm25_retriever.py
│   ├── hybrid_retriever.py
│   └── evaluation.py
│
├── notebooks/
│
├── requirements.txt
│
└── README.md
```

---

# Completed Stages

## Stage 0 — RAG Fundamentals

Learned

- Why LLMs hallucinate
- RAG pipeline
- Dense vs Sparse Retrieval
- Vector Databases
- Embeddings
- Hybrid Retrieval

---

## Stage 1 — Streamlit UI

Built

- Chat Interface
- Session State
- PDF Upload
- Notes Button
- Download Button

---

## Stage 2 — PDF Parsing

Implemented

- PDF extraction
- Text preprocessing
- Header/Footer removal
- Corpus generation
- Page-wise metadata

Output

```python
{
    "page": 4,
    "source": "book.pdf",
    "text": "..."
}
```

---

## Stage 3 — Chunking

Implemented

Custom chunking

- Adjustable chunk size
- Adjustable overlap
- Metadata preservation

Compared against

- LangChain RecursiveCharacterTextSplitter

Output

```python
{
    "chunk_id": 14,
    "page": 5,
    "source": "...",
    "text": "..."
}
```

---

## Stage 4 — Embeddings

Model

```
all-MiniLM-L6-v2
```

Generated

- Chunk embeddings
- Query embeddings
- Vector matrix

---

## Stage 5 — Naive Retriever

Built cosine similarity search completely from scratch.

Pipeline

```
Question
      ↓
Embedding
      ↓
Cosine Similarity
      ↓
Rank Top-K
```

---

## Stage 6 — FAISS

Implemented

- Vector Index
- Semantic Search
- Fast Nearest Neighbor Retrieval

Learned why FAISS improves retrieval speed rather than retrieval quality.

---

## Stage 7 — Hybrid Retrieval

Implemented

- BM25
- Dense Retrieval
- Reciprocal Rank Fusion (RRF)

Pipeline

```
Question
      │
      ├──────────────┐
      ▼              ▼
Dense Search     BM25 Search
      │              │
      └──────┬───────┘
             ▼
     Reciprocal Rank Fusion
             ▼
        Final Ranking
```

---

## Stage 8 — Evaluation Harness

Created

Custom evaluation benchmark containing 20 manually labeled questions.

Compared

- Naive Retriever
- FAISS
- BM25
- Hybrid Retrieval

Metric

- Precision@5

Current Results

| Retriever | Precision@5 |
|------------|------------:|
| Naive Cosine | 0.75 |
| FAISS | 0.75 |
| BM25 | 0.65 |
| Hybrid | 0.75 |

---

# Upcoming

- LLM Generation
- Prompt Engineering
- Chat Memory
- Smart Notes Generation
- PDF Export
- Deployment

---

# What I Learned

Through building this project I learned

- Retrieval-Augmented Generation (RAG)
- Dense Retrieval
- Sparse Retrieval
- Hybrid Retrieval
- Reciprocal Rank Fusion
- Sentence Embeddings
- Cosine Similarity
- FAISS Indexing
- BM25 Ranking
- Evaluation of Retrieval Systems
- PDF Parsing
- Chunking Strategies
- End-to-End ML Project Architecture

---

# Future Improvements

- Query Expansion
- Cross Encoder Re-ranking
- Multi-PDF Support
- Citation Generation
- Source Highlighting
- Better Chunking Strategies
- Advanced Evaluation Metrics

---

## Status

🚧 Work in Progress

Current Progress:

**Stage 8 / Stage 13 Completed**