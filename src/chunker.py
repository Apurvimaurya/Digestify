from pdfparser import extract_pdf_text

def chunk_text(clean_pages, chunk_size, overlap):
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")
    chunks= [] 
    cid=1
    
    for page in clean_pages: 
        start=0
        while start<len(page["text"]):
            end= start + chunk_size
            chunk= page["text"][start:end]
            start= start + chunk_size - overlap
            if not chunk:
                break
            chunks.append({
                "chunk_id": cid,
                "source": page["source"],
                "text": chunk,
                "page": page["page"]
            })
            cid=cid+1
    return chunks

