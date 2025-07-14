import faiss
import os
import openai
from ..utils.embedding import load_faiss_index, embed_query
from ..utils.chunking import get_chunks_for_process

openai.api_key = os.environ.get('OPENAI_API_KEY')

def answer_query(process_id, question, k=3):
    import time
    t0 = time.time()
    index, chunks = load_faiss_index(process_id)
    q_vec = embed_query(question)
    D, I = index.search(q_vec, k)
    retrieval_time = time.time() - t0
    retrieved = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(chunks):
            retrieved.append({
                'chunk': chunks[idx],
                'confidence': float(1.0 / (1.0 + score)) if score > 0 else 1.0
            })
    context = '\n'.join([r['chunk'] for r in retrieved])
    prompt = (
        "You are a helpful assistant. Answer the user's question based only on the following document context. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    t1 = time.time()
    model_name = "gpt-4o"  # or any other model you prefer
    try:
        client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=512            
        )
        answer = response.choices[0].message.content#.strip()
    except Exception as e:
        answer = f"[Error calling LLM: {e}]"
    generation_time = time.time() - t1
    return answer, retrieved, retrieval_time, generation_time, model_name
