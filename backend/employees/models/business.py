from backend.db import db
from datetime import datetime

class Business(db.Model):
    __tablename__ = 'business'

    business_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_contact = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)