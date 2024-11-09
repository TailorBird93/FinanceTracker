from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, TransactionForm, CategoryForm, BudgetForm
from app.models import User, Transaction, Category, Budget
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from sqlalchemy import extract, func
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('index.html', title='Home', transactions=transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    if not categories:
        flash('Please add a category before adding transactions.')
        return redirect(url_for('add_category'))
    form.category.choices = [(c.id, c.name) for c in categories]
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            category_id=form.category.data,
            date=form.date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Your transaction has been added.')
        return redirect(url_for('index'))
    return render_template('add_transaction.html', title='Add Transaction', form=form)


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to edit this transaction.')
        return redirect(url_for('index'))
    form = TransactionForm(obj=transaction)
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.category_id = form.category.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        db.session.commit()
        flash('Transaction updated successfully.')
        return redirect(url_for('index'))
    return render_template('edit_transaction.html', title='Edit Transaction', form=form, transaction=transaction)

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction.')
        return redirect(url_for('index'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully.')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/categories')
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', title='Categories', categories=categories)

@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.')
        return redirect(url_for('categories'))
    return render_template('add_category.html', title='Add Category', form=form)

@app.route('/set_budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    form = BudgetForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        budget = Budget(
            amount=form.amount.data,
            month=form.month.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(budget)
        db.session.commit()
        flash('Budget set successfully.')
        return redirect(url_for('view_budgets'))
    return render_template('set_budget.html', title='Set Budget', form=form)

@app.route('/budgets')
@login_required
def view_budgets():
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return render_template('budgets.html', title='Your Budgets', budgets=budgets)


@app.route('/reports')
@login_required
def reports():
    
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    
    budgets = Budget.query.filter_by(user_id=current_user.id, month=f"{current_year}-{current_month:02}").all()

    report_data = []
    for budget in budgets:
        
        total_spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.category_id == budget.category_id,
            extract('year', Transaction.date) == current_year,
            extract('month', Transaction.date) == current_month
        ).scalar() or 0

        report_data.append({
            'category': budget.category.name,
            'budgeted': budget.amount,
            'spent': total_spent,
            'remaining': budget.amount - total_spent
        })

    return render_template('reports.html', title='Reports', report_data=report_data, month=current_month, year=current_year)
