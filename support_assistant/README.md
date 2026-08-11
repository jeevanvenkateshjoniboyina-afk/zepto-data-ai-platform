# Module 3 – Support Assistant

## Overview

This module implements a Retrieval-Augmented Generation (RAG) style customer support assistant for Zepto.

## Architecture

```
User Query
     │
     ▼
Intent Classification
     │
     ├──────────────┐
     ▼              ▼
Policy Query    General Query
     │              │
     ▼              ▼
ChromaDB      Fixed Response
Retrieval
     │
     ▼
Mock LLM Response
     │
     ▼
JSON Output
```

## Pipeline

### Ingestion

8 Zepto policy documents are stored in the `docs` folder.

### Embedding

Embeddings are generated using:

- sentence-transformers
- all-MiniLM-L6-v2

### Retrieval

Embeddings are stored inside ChromaDB.

Top-3 relevant documents are retrieved using cosine similarity.

### Generation

The LangGraph workflow routes each query.

- Policy questions → Retrieval
- General questions → Direct response

### MOCK_LLM

Default:

```
MOCK_LLM = 1
```

No external LLM API is required.

## API

```
POST /ask
```

Example request:

```json
{
    "query":"What is the delivery fee?"
}
```

Example response:

```json
{
    "answer":"Based on the retrieved context...",
    "sources":[
        "doc_01",
        "doc_05",
        "doc_02"
    ],
    "confidence":1
}
```