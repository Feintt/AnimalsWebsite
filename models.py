from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
database = SQLAlchemy(app)


class User(database.Model):
    ID = database.Column(database.Integer, primary_key=True)
    full_name = database.Column(database.String(80), unique=False, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String(80), unique=False, nullable=False)
    posted_pets = database.relationship('Pet', backref='user', lazy=True)


class Pet(database.Model):
    ID = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80), unique=True, nullable=False)
    age = database.Column(database.Integer, unique=False, nullable=False)
    bio = database.Column(database.String(80), unique=False, nullable=False)
    posted_by = database.Column(database.Integer, database.ForeignKey('user.ID'), nullable=True)


database.create_all()
