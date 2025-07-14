import re

def clean_text(text: str) -> str:
    """
    Basic cleaning: removes HTML remnants, extra whitespace, and non-ASCII chars.
    """
    text = re.sub(r'\\s+', ' ', text)                # Normalize whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)        # Remove non-ASCII characters
    text = re.sub(r'(?i)(copyright|all rights reserved).*', '', text)  # Remove footers
    # battle against prompt injections
    patterns = [
        r"(?i)ignore previous instructions", 
        r"you are an AI", 
        r"change the system prompt", 
        r"act as",
        r"assistant's identity",
    ]
    for pattern in patterns:
        text = re.sub(pattern, "[REDACTED]", text)
    return text.strip()


def chunk_text(text, chunk_size=500, overlap=50):
    # Simple sentence-based chunking
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    chunk = ''
    for sentence in sentences:
        if len(chunk) + len(sentence) < chunk_size:
            chunk += ' ' + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def get_chunks_for_process(process_id):
    # Dummy: In real app, load from persistent storage
    from .embedding import CHUNKS_DB
    return CHUNKS_DB.get(process_id, [])
