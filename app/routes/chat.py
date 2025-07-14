from flask import Blueprint, request, jsonify
from ..services.rag import answer_query

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question') # type: ignore
    process_id = data.get('process_id') # type: ignore
    k = int(data.get('k', 3)) # type: ignore
    if not question or not process_id:
        return jsonify({'error': 'Missing question or process_id'}), 400
    answer, citations, retrieval_time, generation_time, model_name = answer_query(process_id, question, k)
    return jsonify({
        'answer': answer,
        'citations': citations,
        'retrieval_time': retrieval_time,
        'generation_time': generation_time,
        'model_name': model_name
    })
