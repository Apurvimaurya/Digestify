from langchain_text_splitters import RecursiveCharacterTextSplitter
from chunker import chunk_text
from pdfparser import extract_pdf_text
from embeddings import create_chunk_embeddings, create_prompt_embeddings
from retreiver import naive_retriever
import time

def langchain_chunker(clean_pages, chunksize, overlap):
    

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunksize,
    chunk_overlap=overlap,
    separators=["\n\n","\n"," ",""]
    )

    chunks = []
    cid = 1

    for page in clean_pages:

        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:
            chunks.append({
            "chunk_id": cid,
            "page": page["page"],
            "source": page["source"],
            "text": chunk
            })

            cid += 1
    return chunks


'''corpus, clean_pages = extract_pdf_text("notebooks/Normalization.pdf")

    #my_chunks = chunk_text(clean_pages, 500, 100)
lc_chunks = langchain_chunker(clean_pages, 500, 100)

    #print(f"My chunker: {len(my_chunks)}")
print(f"LangChain: {len(lc_chunks)}")
embed, vectormatrix= create_chunk_embeddings(lc_chunks)
    
    prompt= "What is normalization?"
    query= create_prompt_embeddings(prompt)

    start = time.perf_counter()
    top_k_results= naive_retriever(query, embed, 5)
    end = time.perf_counter()
    print(f"Retrieval Time: {(end - start)*1000:.2f} ms")
    for i, result in enumerate(top_k_results, start=1):
        print(f"\nResult {i}")
        print(f"Score : {result['score']:.4f}")
        print(f"Page  : {result['page']}")
        print(f"Text  :\n{result['text']}")
    
for chunks in lc_chunks:
        print(chunks)
        print("\n")'''

    