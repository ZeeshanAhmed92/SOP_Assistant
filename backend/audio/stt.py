from flask import Blueprint, request, jsonify
import speech_recognition as sr
import os

stt_bp = Blueprint('stt', __name__)
recognizer = sr.Recognizer()

@stt_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    temp_path = os.path.join('uploads', audio_file.filename)
    audio_file.save(temp_path)

    with sr.AudioFile(temp_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'error': 'Speech not recognized'}), 400
        except sr.RequestError:
            return jsonify({'error': 'STT service failed'}), 500