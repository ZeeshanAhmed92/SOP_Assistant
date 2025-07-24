from flask import Blueprint, request, jsonify
from configs.db import db
from datetime import datetime

log_bp = Blueprint('logs', __name__)

class CheckLog(db.Model):
    __tablename__ = 'check_log'

    check_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, nullable=False)
    check_time = db.Column(db.DateTime, default=datetime.utcnow)
    access_type = db.Column(db.String(50))  # voice, text, admin, etc.

class SOPLog(db.Model):
    __tablename__ = 'sop_log'

    log_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    interaction_time = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Text)

@log_bp.route('/check-in', methods=['POST'])
def log_checkin():
    data = request.json
    log = CheckLog(
        employee_id=data['employee_id'],
        location_id=data['location_id'],
        access_type=data.get('access_type', 'voice')
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Check-in logged'})

@log_bp.route('/sop-interaction', methods=['POST'])
def log_sop_interaction():
    data = request.json
    log = SOPLog(
        employee_id=data['employee_id'],
        question_text=data['question_text'],
        feedback=data.get('feedback')
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'SOP interaction logged'})