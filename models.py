# models.py
# import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

class WeatherRecord(db.Model):
    _tablename_ = "weather_records"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location_text = db.Column(db.String(200), nullable=False)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    payload_json = db.Column(db.Text, nullable=False)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "location_text": self.location_text,
            "lat": self.lat,
            "lon": self.lon,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "payload": json.loads(self.payload_json)
        }