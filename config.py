import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# fix the DATABASE_URL for SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
# Initialize the database
db = SQLAlchemy(app)
