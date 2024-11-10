import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# fix the DATABASE_URL for SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended setting to avoid warnings

# Initialize the database
db = SQLAlchemy(app)
