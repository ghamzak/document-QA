<<<<<<< HEAD
# document-QA
Upload your personal documents and chat with them (ask questions)
=======
# RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) web app for chatting with PDF documents using Flask, Sentence Transformers, FAISS, and OpenTelemetry for observability.

## Features
- Upload and chat with PDF documents
- Preprocessing, chunking, and embedding with Sentence Transformers
- Vector storage and retrieval with FAISS
- UI chatbot with chunk provenance display
- Query rewriting and prompt engineering for robust RAG
- Observability with OpenTelemetry, Prometheus, Loki, and Grafana
- Logging of latency for embedding, retrieval, and LLM generation
- Testing and monitoring

## Directory Structure
```
app/
  routes/
  services/
  utils/
  templates/
  static/
docs/
tests/
observability/
Dockerfile
docker-compose.yml
.env
README.md
```

## Setup
See `docs/` for detailed setup and usage instructions.
>>>>>>> b97f784 (local app initial commit)
