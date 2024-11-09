from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)
app.config.from_object(Config)

db = SQLAlchemy(app)

from app import routes, models
