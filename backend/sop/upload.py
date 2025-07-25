from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from sop.processor import process_document,delete_document

import os

sop_upload_bp = Blueprint('sop_upload', __name__)
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt'}

def is_allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

@sop_upload_bp.route('/upload', methods=['POST'])
def upload_sop():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        
        if not is_allowed_file(filename):
            return jsonify({'error': 'Only PDF, DOC, DOCX, or TXT files are allowed'}), 400

        file_path = os.path.join(UPLOAD_FOLDER, filename)

        

        file.save(file_path)
        result = process_document(file_path)  # renamed from process_pdf
        return jsonify({'message': result, 'path': file_path})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@sop_upload_bp.route('/delete', methods=['POST'])
def delete_sop():
    data = request.get_json()
    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400

    filename = secure_filename(data['filename'])
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File does not exist'}), 404

    try:
        delete_document(file_path)
        os.remove(file_path)
        return jsonify({'message': 'File deleted successfully', 'path': file_path})
    except Exception as e:
        return jsonify({'error': f'Could not delete file: {str(e)}'}), 500
