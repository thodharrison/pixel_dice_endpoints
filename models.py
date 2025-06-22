from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# This gets initialized in app.py
db = SQLAlchemy()

class Roll(db.Model):
    __tablename__ = 'roll'

    id = db.Column(db.Integer, primary_key=True, )
    value = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Roll id={self.id} value={self.value} timestamp={self.timestamp}>"

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    pixelId = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)

