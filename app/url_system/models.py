from app import db
from datetime import datetime

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2083), nullable=False)
    short_id = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expiration_time = db.Column(db.DateTime,default=24, nullable=True)
    access_count = db.Column(db.Integer, default=0, nullable=False)

class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(10), db.ForeignKey('url_mapping.short_id'), nullable=False)
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)