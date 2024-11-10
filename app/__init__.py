from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


login = LoginManager(app)
login.login_view = 'main.login'  


from app.models import User

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app.routes import main as main_blueprint
app.register_blueprint(main_blueprint)
