from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

    devices = db.relationship('DeviceSelection', backref='user', lazy=True)

class DeviceSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # ex: 'Switch', 'Hub', 'PC', 'Server', etc.
