from flask import Blueprint, request, jsonify

sop_query_bp = Blueprint('sop_query', __name__)

@sop_query_bp.route('/query', methods=['POST'])
def query_sop():
    data = request.json
    question = data.get('question')

    # Dummy response (to be replaced by RAG logic)
    response = f"This is a placeholder response for: '{question}'"
    return jsonify({'response': response})