# -*- coding: utf-8 -*-
import argparse
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
rag_qa_path = os.path.dirname(current_dir)
project_root = os.path.dirname(rag_qa_path)

for path in (current_dir, rag_qa_path, project_root):
    if path not in sys.path:
        sys.path.insert(0, path)

from base import logger
from document_processor import process_documents
from vector_store import VectorStore


def ingest_documents(directory_path, source=None, dry_run=False):
    directory_path = os.path.abspath(directory_path)
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Document directory not found: {directory_path}")

    chunks = process_documents(directory_path)
    if source:
        for chunk in chunks:
            chunk.metadata["source"] = source

    if not chunks:
        logger.warning(f"No documents found for ingestion: {directory_path}")
        return 0

    logger.info(f"Prepared {len(chunks)} chunks from {directory_path}")
    if dry_run:
        logger.info("Dry run enabled, skip Milvus upsert")
        return len(chunks)

    vector_store = VectorStore()
    vector_store.add_documents(chunks)
    logger.info(f"Ingested {len(chunks)} chunks into Milvus")
    return len(chunks)


def main():
    parser = argparse.ArgumentParser(description="Ingest new documents into Milvus.")
    parser.add_argument("--dir", required=True, help="Directory that contains new documents.")
    parser.add_argument("--source", default=None, help="Source label, for example: problem.")
    parser.add_argument("--dry-run", action="store_true", help="Only parse and split documents.")
    args = parser.parse_args()

    count = ingest_documents(args.dir, source=args.source, dry_run=args.dry_run)
    print(f"chunks={count}")


if __name__ == "__main__":
    main()
