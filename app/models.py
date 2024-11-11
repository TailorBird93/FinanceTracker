
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, index=True, nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='transactions', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.amount} - {self.category.name}>'
    
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7), nullable=False)  
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    category = db.relationship('Category', backref='budgets')
    user = db.relationship('User', backref='budgets')

    __table_args__ = (
        UniqueConstraint('user_id', 'category_id', 'month', name='uix_user_category_month'),
    )

    def __repr__(self):
        return f'<Budget {self.amount} for {self.category.name} in {self.month}>'


