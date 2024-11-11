from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models import User

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'main.login'

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        from app.routes import main as main_blueprint  
        app.register_blueprint(main_blueprint)  

        from app import models  

    return app
