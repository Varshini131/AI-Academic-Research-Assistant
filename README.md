# AI Academic Research Assistant

An intermediate-level academic research agent prototype built with Python and Streamlit.

## Features

- Search arXiv for papers by topic.
- Display titles, authors, abstracts, dates, and source links.
- Upload research-paper PDFs and extract selectable text.
- Ask questions over uploaded PDFs and selected paper abstracts.
- Compare two or more sources in a structured table.
- Draft a literature review with themes, limitations, tentative research gaps, and references.
- Download literature review drafts as Markdown.

## Architecture

```text
User
 |
 v
Streamlit UI
 |
 +--> Paper Search Tool ----> arXiv API
 |
 +--> PDF Reader Tool ------> PyMuPDF
 |
 +--> Research Q&A Tool ----+
 |
 +--> Comparison Tool ------+--> LLM API (Groq, optional)
 |
 +--> Literature Review Tool+
```

The prototype uses a tool-based workflow with explicit task prompts. It is not an unconstrained autonomous agent. Its tools and stages are clearly separated so you can explain and extend the architecture for your ML project.

## Requirements

- Python 3.10 or newer
- Internet connection for arXiv search and LLM calls
- A Groq API key for AI-generated answers, comparisons, and literature reviews. Paper search and PDF extraction work without a key.

## Run locally (Windows / VS Code)

1. Extract the ZIP and open the `ai_academic_research_assistant` folder in VS Code.
2. Open a terminal in that folder.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `.venv\Scripts\activate.bat` from Command Prompt instead.

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and paste your own Groq API key. Do not share or commit `.env`.

6. Start the app:

   ```powershell
   streamlit run app.py
   ```

7. Streamlit will show a local URL, usually `http://localhost:8501`.

## Suggested demo

1. Search for `retrieval augmented generation`.
2. Add two or more paper abstracts to the research set.
3. Upload a research PDF and extract its text.
4. Ask: `What problem does this paper address, and what limitations are mentioned?`
5. Compare two or more sources.
6. Generate a literature review and download the Markdown draft.

## Important limitations

- arXiv search covers arXiv, not all academic publishers.
- Scanned/image-only PDFs need OCR, which is not included in this first version.
- The app truncates source text sent to the model to control context size.
- AI outputs may be wrong. Verify claims, methods, publication details, and references against original papers.
- Research gaps are hypotheses to investigate, not a guarantee that a gap is novel.
- Do not upload papers or material unless you have permission to process them.

## Next upgrades

- Add Semantic Scholar search and DOI metadata.
- Add embedding-based retrieval (Sentence Transformers + FAISS) so questions retrieve only relevant chunks.
- Add page/section-aware citations and source snippets.
- Add export to PDF and a saved project workspace.
- Add tests for search parsing, PDF extraction, and prompt construction.
