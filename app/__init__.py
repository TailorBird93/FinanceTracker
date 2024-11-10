from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' 

    # Register blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
