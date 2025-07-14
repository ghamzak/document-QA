from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os

MODEL = SentenceTransformer('all-MiniLM-L6-v2')
FAISS_DIR = os.path.join(os.getcwd(), 'app', 'static', 'faiss')
CHUNKS_DB = {}

os.makedirs(FAISS_DIR, exist_ok=True)

def embed_chunks(chunks):
    vectors = MODEL.encode(chunks, show_progress_bar=True)
    return np.array(vectors, dtype='float32')

def save_faiss_index(process_id, vectors, chunks):
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors) # type: ignore
    faiss.write_index(index, os.path.join(FAISS_DIR, f'{process_id}.index'))
    CHUNKS_DB[process_id] = chunks

def load_faiss_index(process_id):
    index = faiss.read_index(os.path.join(FAISS_DIR, f'{process_id}.index'))
    chunks = CHUNKS_DB.get(process_id, [])
    return index, chunks

def embed_query(query):
    vec = MODEL.encode([query])
    return np.array(vec, dtype='float32')
