from ..services.preprocess import list_processed_docs
from flask import Blueprint, request, jsonify, current_app, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename
from ..services.preprocess import process_pdf

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/api/docs', methods=['GET'])
def docs_list():
    return jsonify(list_processed_docs())
@upload_bp.route('/')
def index():
    return render_template('index.html')

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.lower().endswith('.pdf'): # type: ignore
        filename = secure_filename(file.filename) # type: ignore
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        # Start processing (chunk, embed, index)
        process_id = process_pdf(file_path)
        return jsonify({'message': 'File uploaded', 'process_id': process_id}), 200
    return jsonify({'error': 'Invalid file type'}), 400

@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
