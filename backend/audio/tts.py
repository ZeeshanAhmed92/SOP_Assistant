from flask import Blueprint, request, send_file, jsonify
from gtts import gTTS
import os
import uuid

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    filename = f"tts_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join('uploads', filename)

    tts = gTTS(text)
    tts.save(filepath)

    return send_file(filepath, mimetype='audio/mpeg')
