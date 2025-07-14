from flask import Blueprint, jsonify
from ..services.preprocess import get_process_status

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/api/progress/<process_id>')
def progress(process_id):
    status = get_process_status(process_id)
    return jsonify(status)
