import streamlit as st

from src.pdfparser import extract_pdf_text
from src.chunker import chunk_text
from src.embeddings import (
    create_chunk_embeddings,
    create_prompt_embeddings
)
from src.hybrid_retriever import hybrid_retriever
from src.llm import get_response
from src.faiss_retriever import faiss_retriever
from src.llm_judge import judge_faithfullness
from src.Notes_gen import notes_generator
from src.topic_cluster import deduplication
from src.notes_pdf import notes_pdf_gen
import json
# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "notes" not in st.session_state:
    st.session_state.notes = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "chunk_embeddings" not in st.session_state:
    st.session_state.chunk_embeddings = None

if "vector_matrix" not in st.session_state:
    st.session_state.vector_matrix = None

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history= []


# ---------------- TITLE ---------------- #

st.title("DIGESTIFY")


# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📚 Your AI Study Mate!")

uploaded_file = st.sidebar.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)

# Process PDF ONLY ONCE
if uploaded_file is not None:

    if st.session_state.processed_file != uploaded_file.name:

        with st.spinner("Processing PDF..."):

            corpus, clean_pages = extract_pdf_text(uploaded_file)

            chunks = chunk_text(
                clean_pages,
                chunk_size=500,
                overlap=100
            )

            chunk_embeddings, vector_matrix = create_chunk_embeddings(chunks)

            st.session_state.chunks = chunks
            st.session_state.chunk_embeddings = chunk_embeddings
            st.session_state.vector_matrix = vector_matrix

            st.session_state.processed_file = uploaded_file.name
            st.session_state.uploaded_file = uploaded_file

        st.sidebar.success("PDF processed successfully!")

# ---------------- CHAT HISTORY ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ---------------- #

if st.session_state.chunks is not None:

    prompt = st.chat_input("Ask a question...")

    if prompt:

        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        query_embedding = create_prompt_embeddings(prompt)

        top_chunks = hybrid_retriever(
            st.session_state.chunks,
            prompt,
            5,
            query_embedding,
            st.session_state.chunk_embeddings,
            st.session_state.vector_matrix,
            
        )

        with st.spinner("Thinking..."):
            response = get_response(prompt, top_chunks)
            faithfullness= judge_faithfullness(prompt, top_chunks, response)
            result= json.loads(faithfullness.text)
            

        with st.chat_message("assistant"):
            st.markdown(response)
            st.write(f"> {result["label"]}")
            st.write(f"> {result["reason"]}")
           

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.session_state.chat_history.append(
            {
                "Question": prompt,
                "Answer": response,
                "Retrieved_chunks":top_chunks,
                "Faithfulness": result["label"],
                "Reason": result["reason"]
            }
        )

else:

    st.info("Upload a PDF to begin chatting.")


# ---------------- NOTES ---------------- #
pdf_buffer=""
if st.sidebar.button("Generate Notes", width=400):

    if st.session_state.messages:
        questions = [item["Question"]for item in st.session_state.chat_history]
        clusters= deduplication(questions,0.85, st.session_state.chat_history )
        structured_notes= notes_generator(clusters)
        pdf_buffer= notes_pdf_gen(structured_notes)
        st.session_state.notes= pdf_buffer
        if pdf_buffer:
            st.success("Notes Generated!")
        else:
            st.error("Failed to Generate Notes")
    else:
        st.sidebar.error("Start a chat first.")
    if st.session_state.notes:
        if st.download_button(
        label="📥 Download Smart Notes",
        data=pdf_buffer,
        file_name="Digestify_Notes.pdf",
        mime="application/pdf", width=800
        ):
            st.success("Notes Downloaded!")
        



        
