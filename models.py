from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(170))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=False)
    color = db.Column(db.String(30), unique=False)
    year = db.Column(db.Integer, unique=False)
    make = db.Column(db.String(30), unique=False)
    price = db.Column(db.Integer, nullable=True)
