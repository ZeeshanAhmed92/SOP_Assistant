from configs.db import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.business_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    dob = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)