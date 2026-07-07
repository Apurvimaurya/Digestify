from langchain_text_splitters import RecursiveCharacterTextSplitter
from chunker import chunk_text
from pdfparser import extract_pdf_text

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

if __name__ == "__main__":
    corpus, clean_pages = extract_pdf_text("notebooks/Normalization.pdf")

    my_chunks = chunk_text(clean_pages, 500, 100)
    lc_chunks = langchain_chunker(clean_pages, 500, 100)

    print(f"My chunker: {len(my_chunks)}")
    print(f"LangChain: {len(lc_chunks)}")