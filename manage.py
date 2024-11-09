
from app import app, db
from app.models import User, Transaction, Category
from flask_migrate import Migrate, upgrade

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transaction': Transaction, 'Category': Category}
