import hashlib
from datetime import datetime, timedelta
from .models import URLMapping, AccessLog
from app import db

BASE_URL = "https://short.ly"

def generate_short_id(original_url):
    hash_object = hashlib.md5(original_url.encode())
    return hash_object.hexdigest()[:6]

def process_short_url_request(original_url, expiration_time):
    try:
        expiration_hours = int(expiration_time) if expiration_time else 24
    except ValueError:
        expiration_hours = 24

    existing_mapping = URLMapping.query.filter_by(original_url=original_url).first()
    if existing_mapping:
        if expiration_time:
            existing_mapping.expiration_time = datetime.utcnow() + timedelta(hours=expiration_hours)
        short_id = existing_mapping.short_id
        db.session.commit()
    else:
        short_id = generate_short_id(original_url)
        expiration_time = datetime.utcnow() + timedelta(hours=expiration_hours)

        new_mapping = URLMapping(
            original_url=original_url,
            short_id=short_id,
            expiration_time=expiration_time
        )
        db.session.add(new_mapping)
        db.session.commit()

    return f"{BASE_URL}/{short_id}"

def get_redirect_mapping(short_id):
    mapping = URLMapping.query.filter_by(short_id=short_id).first()
    if not mapping or mapping.expiration_time < datetime.utcnow():
        return None
    mapping.access_count = mapping.access_count + 1 if mapping.access_count else 1
    db.session.commit()
    return mapping

def log_access(short_id, ip_address):
    access_log = AccessLog(short_id=short_id, ip_address=ip_address)
    db.session.add(access_log)
    db.session.commit()

def get_analytics_data(short_id):
    mapping = URLMapping.query.filter_by(short_id=short_id).first()
    if not mapping:
        return None

    access_logs = AccessLog.query.filter_by(short_id=short_id).all()
    return {
        "short_url": f"{BASE_URL}/{short_id}",
        "original_url": mapping.original_url,
        "created_at": mapping.created_at,
        "access_count": mapping.access_count or 0,
        "logs": [
            {"ip_address": log.ip_address, "timestamp": log.accessed_at}
            for log in access_logs
        ]
    }
