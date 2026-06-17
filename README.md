# Integrated QA System

An enterprise knowledge-base question answering system built with FastAPI, MySQL, Redis, Milvus, hybrid retrieval, reranking, and an OpenAI-compatible LLM interface.

This public version is sanitized for portfolio and interview review. Enterprise documents, logs, local configuration, model weights, training checkpoints, and private runtime files are intentionally excluded.

## Features

- Structured QA matching with MySQL, Redis cache, and BM25.
- RAG fallback when no high-confidence structured answer is found.
- Document ingestion for PDF, Word, PowerPoint, images, Markdown, and text files.
- Chinese-aware recursive text splitting with parent-child chunk structure.
- BGE-M3 dense and sparse embeddings.
- Milvus hybrid vector search with weighted dense/sparse recall.
- CrossEncoder reranking with BGE reranker.
- Query classification for general knowledge and professional consultation.
- Query strategy selection, including direct search, sub-query search, backtracking search, and HyDE.
- FastAPI service with WebSocket streaming.
- Session-level conversation history stored in MySQL.

## Architecture

```text
User / Web UI
    |
FastAPI app.py
    |
IntegratedQASystem
    |
    |-- BM25Search -> Redis cache -> MySQL QA table
    |
    |-- RAGSystem
          |
          |-- QueryClassifier
          |-- StrategySelector
          |-- VectorStore -> Milvus hybrid search
          |-- BGE reranker
          |-- OpenAI-compatible LLM service
```

## Project Structure

```text
.
|-- app.py                  # Main FastAPI web service
|-- api.py                  # SSE API variant kept for reference
|-- new_main.py             # Integrated QA orchestration
|-- config.example.ini      # Configuration template
|-- requirements.txt        # Python dependencies
|-- use_api.py              # API client example
|-- base/                   # Config and logging utilities
|-- mysql_qa/               # MySQL, Redis, BM25 modules
|-- rag_qa/
|   |-- core/               # RAG, vector store, prompts, classifier, ingestion
|   |-- edu_document_loaders/
|   |-- edu_text_spliter/
|-- static/                 # Static web page
```

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy the configuration template:

```bash
copy config.example.ini config.ini
```

3. Update `config.ini` with local MySQL, Redis, Milvus, and LLM service settings.

4. Start the API service:

```bash
python app.py
```

Default local address:

```text
http://127.0.0.1:8000
```

## Document Ingestion

The ingestion workflow is implemented in `rag_qa/core/document_processor.py` and `rag_qa/core/vector_store.py`.

Run ingestion for a directory:

```bash
python rag_qa/core/ingest_new_documents.py --dir path/to/docs --source problem
```

Dry run without writing to Milvus:

```bash
python rag_qa/core/ingest_new_documents.py --dir path/to/docs --source problem --dry-run
```

## Notes

- `config.ini` is ignored and should not be committed.
- Enterprise documents and model weights are excluded from this public version.
- Local model service can be connected through an OpenAI-compatible `base_url`.
- For production deployment, add authentication, user-level session ownership, stricter CORS rules, container orchestration, monitoring, and backup strategy.
