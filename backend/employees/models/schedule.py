from configs.db import db
from datetime import datetime

class Schedule(db.Model):
    __tablename__ = 'schedule'

    schedule_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    shift_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
