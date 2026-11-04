import io
import xml.etree.ElementTree as ET
import requests
import fitz

ARXIV_API = "https://export.arxiv.org/api/query"

def search_arxiv(query: str, max_results: int = 5):
    """Search arXiv Atom API and return normalized paper records."""
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    response = requests.get(ARXIV_API, params=params, timeout=25)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    for entry in root.findall("atom:entry", ns):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ns)).split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ns)).split())
        authors = [a.findtext("atom:name", default="", namespaces=ns) for a in entry.findall("atom:author", ns)]
        url = entry.findtext("atom:id", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)
        paper_id = url.rstrip("/").split("/")[-1] if url else ""
        papers.append({
            "id": paper_id,
            "title": title,
            "summary": summary,
            "authors": authors,
            "url": url,
            "published": published,
        })
    return papers

def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract selectable text from a PDF byte stream."""
    text_parts = []
    with fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf") as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text_parts.append(f"[Page {page_num}]\n{page_text}")
    return "\n\n".join(text_parts)

def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 150):
    """Simple overlapping chunks for a future retrieval-augmented generation step."""
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks
