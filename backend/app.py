from flask import Flask
from flask_cors import CORS
from configs.db import init_db # 👈 import init_db
from auth.routes import auth_bp
from employees.routes import emp_bp
from sop.upload import sop_upload_bp
from sop.query import sop_query_bp
from audio.stt import stt_bp
from audio.tts import tts_bp
from logs.routes import log_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("./configs/configurations.py")  # or use environment variables
    CORS(app)

    init_db(app)  # 👈 initialize DB with app context

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(emp_bp, url_prefix='/employee')
    app.register_blueprint(sop_upload_bp, url_prefix='/sop')
    app.register_blueprint(sop_query_bp, url_prefix='/assistant')
    app.register_blueprint(stt_bp, url_prefix='/audio')
    app.register_blueprint(tts_bp, url_prefix='/audio')
    app.register_blueprint(log_bp, url_prefix='/logs')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
