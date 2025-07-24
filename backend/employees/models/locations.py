from backend.db import db
from datetime import datetime

class Location(db.Model):
    __tablename__ = 'location'

    location_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.business_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    timezone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
