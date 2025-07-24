from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

sop_upload_bp = Blueprint('sop_upload', __name__)
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@sop_upload_bp.route('/upload', methods=['POST'])
def upload_sop():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'path': file_path})
