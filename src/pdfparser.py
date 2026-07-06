from pypdf import PdfReader
import os
from collections import Counter


def clean_txt(text):
    text = " ".join(text.split())          # remove extra spaces/newlines
    text = text.replace("\uf0a7", "•")     # replace weird bullet
    return text


def remove_headers_footers(raw_pages):
    headers = []
    footers = []
    # Collect first and last lines from every page
    for page in raw_pages:
        lines = page["text"].splitlines()

        if not lines:
            continue

        headers.append(lines[0].strip())
        footers.append(lines[-1].strip())

    header_counts = Counter(headers)
    footer_counts = Counter(footers)
    repeat_threshold = len(raw_pages) * 0.7

    headers_to_remove = {
        line
        for line, count in header_counts.items()
        if count >= repeat_threshold
    }

    footers_to_remove = {
        line
        for line, count in footer_counts.items()
        if count >= repeat_threshold
    }

    cleaned_pages = []

    for page in raw_pages:
        lines = page["text"].splitlines()

        lines = [
            line
            for line in lines
            if line.strip() not in headers_to_remove
            and line.strip() not in footers_to_remove
        ]

        cleaned_pages.append({
            "page": page["page"],
            "source": page["source"],
            "text": "\n".join(lines)
        })

    return cleaned_pages


def preprocess(text):
    return clean_txt(text)


def extract_pdf_text(file):
    reader = PdfReader(file)
    file_name = os.path.basename(file)

    raw_pages = []

    # Build raw page list
    for page_num, page in enumerate(reader.pages):
        raw_pages.append({
            "page": page_num + 1,
            "source": file_name,
            "text": page.extract_text() or ""
        })

    # Remove headers and footers
    clean_pages = remove_headers_footers(raw_pages)

    # Preprocess text and build corpus
    corpus = ""

    for page in clean_pages:
        page["text"] = preprocess(page["text"])
        corpus += page["text"] + "\n"

    return corpus, clean_pages


corpus, pages = extract_pdf_text(r"notebooks\Normalization.pdf")

print(corpus)
print("\n----------------------------\n")
print(pages)