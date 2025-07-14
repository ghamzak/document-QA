import uuid
import os
from PyPDF2 import PdfReader
from ..utils.chunking import chunk_text
from ..utils.embedding import embed_chunks, save_faiss_index


PROCESS_STATUS = {}
PROCESSED_DOCS = {}  # filename -> process_id

# This is a simple in-memory process tracker for demo purposes

def process_pdf(file_path):
    filename = os.path.basename(file_path)
    if filename in PROCESSED_DOCS:
        # Already processed, return existing process_id
        process_id = PROCESSED_DOCS[filename]
        PROCESS_STATUS[process_id]['status'] = 'ready'
        PROCESS_STATUS[process_id]['progress'] = 100
        return process_id
    process_id = str(uuid.uuid4())
    PROCESSED_DOCS[filename] = process_id
    PROCESS_STATUS[process_id] = {'status': 'processing', 'progress': 0, 'filename': filename}
    # 1. Read PDF
    text = read_pdf(file_path)
    PROCESS_STATUS[process_id]['progress'] = 20
    # 2. Clean and chunk
    chunks = chunk_text(text)
    PROCESS_STATUS[process_id]['progress'] = 50
    # 3. Embed
    vectors = embed_chunks(chunks)
    PROCESS_STATUS[process_id]['progress'] = 80
    # 4. Store in FAISS
    save_faiss_index(process_id, vectors, chunks)
    PROCESS_STATUS[process_id]['progress'] = 100
    PROCESS_STATUS[process_id]['status'] = 'ready'
    return process_id
def list_processed_docs():
    # Returns a list of (filename, process_id)
    return [{'filename': fn, 'process_id': pid} for fn, pid in PROCESSED_DOCS.items()]

def get_process_status(process_id):
    return PROCESS_STATUS.get(process_id, {'status': 'not_found', 'progress': 0})

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
