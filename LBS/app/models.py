from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Meter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Meter {self.label}>'


class MeterData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.Integer, db.ForeignKey('meter.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    meter = db.relationship('Meter', backref=db.backref('meter_data', lazy=True))

    def __repr__(self):
        return f'<MeterData {self.value} at {self.timestamp}>'
