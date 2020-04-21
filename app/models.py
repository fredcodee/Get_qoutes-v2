from flask_login import UserMixin
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(100))
  qoutes = db.relationship('Favourites', backref='fav', lazy=True)


class Favourites(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  qoute = db.Column(db.String)
