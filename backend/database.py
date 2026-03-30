from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    password    = db.Column(db.String(200), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    generations = db.relationship('Generation', backref='user', lazy=True)

class Generation(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt     = db.Column(db.Text, nullable=False)
    rows       = db.Column(db.Integer, nullable=False)
    columns    = db.Column(db.Integer, nullable=False)
    filename   = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
