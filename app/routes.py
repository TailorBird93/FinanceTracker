from flask import Blueprint, abort, render_template, flash, redirect, url_for, request
from . import db
from .forms import (
    LoginForm,
    RegistrationForm,
    TransactionForm,
    CategoryForm,
    BudgetForm,
    ChangePasswordForm,
    UpdateProfileForm
)
from .models import User, Transaction, Category, Budget
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from sqlalchemy import extract, func
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter

# Define a blueprint
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TransactionForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    search_description = request.args.get('description', '', type=str)
    search_category = request.args.get('category', 0, type=int)
    search_start_date = request.args.get('start_date', '', type=str)
    search_end_date = request.args.get('end_date', '', type=str)
    
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10  
    
    
    transactions_query = Transaction.query.filter_by(user_id=current_user.id)
    
    if search_description:
        transactions_query = transactions_query.filter(Transaction.description.ilike(f"%{search_description}%"))
    if search_category:
        transactions_query = transactions_query.filter_by(category_id=search_category)
    if search_start_date:
        transactions_query = transactions_query.filter(Transaction.date >= search_start_date)
    if search_end_date:
        transactions_query = transactions_query.filter(Transaction.date <= search_end_date)
    
    transactions_query = transactions_query.order_by(Transaction.date.desc())
    
    total = transactions_query.count()
    
    transactions = transactions_query.paginate(page=page, per_page=per_page, error_out=False).items
    
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    
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
        return redirect(url_for('main.index'))
    
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    return render_template(
        'index.html', 
        title='Home', 
        transactions=transactions,
        categories=categories,
        search_description=search_description,
        search_category=search_category,
        search_start_date=search_start_date,
        search_end_date=search_end_date,
        pagination=pagination,
        form=form
    )

@main.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    if not categories:
        flash('Please add a category before adding transactions.')
        return redirect(url_for('main.add_category'))
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
        return redirect(url_for('main.index'))
    return render_template('add_transaction.html', title='Add Transaction', form=form)


@main.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to edit this transaction.')
        return redirect(url_for('main.index'))
    form = TransactionForm(obj=transaction)
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        transaction.amount = form.amount.data
        transaction.category_id = form.category.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        db.session.commit()
        flash('Transaction updated successfully.')
        return redirect(url_for('main.index'))
    return render_template('edit_transaction.html', title='Edit Transaction', form=form, transaction=transaction)

@main.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction.')
        return redirect(url_for('main.index'))
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully.')
    return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/categories')
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', title='Categories', categories=categories)

@main.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.')
        return redirect(url_for('main.categories'))
    return render_template('add_category.html', title='Add Category', form=form)

@main.route('/set_budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    form = BudgetForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        selected_month = form.month.data
        print(f"Selected Month: {selected_month}") 
        
        
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            category_id=form.category.data,
            month=selected_month
        ).first()
        
        if existing_budget:
            flash('A budget for this category and month already exists.')
            return redirect(url_for('main.set_budget'))
        
        budget = Budget(
            amount=form.amount.data,
            month=selected_month,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(budget)
        
        try:
            db.session.commit()
            flash('Budget set successfully.')
            return redirect(url_for('main.view_budgets'))
        except IntegrityError:
            db.session.rollback()
            flash('A budget for this category and month already exists.')
            return redirect(url_for('main.set_budget'))
    
    return render_template('set_budget.html', title='Set Budget', form=form)

@main.route('/budgets')
@login_required
def view_budgets():
    from flask_paginate import Pagination, get_page_parameter

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10 
    
    budgets_query = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.month.desc())
    total = budgets_query.count()
    budgets = budgets_query.paginate(page=page, per_page=per_page, error_out=False).items
    
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')
    
    return render_template('budgets.html', title='Your Budgets', budgets=budgets, pagination=pagination)

@main.route('/reports')
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


@main.route('/edit_budget/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.user_id != current_user.id:
        flash('You do not have permission to edit this budget.')
        return redirect(url_for('main.view_budgets'))
    form = BudgetForm(obj=budget)
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            category_id=form.category.data,
            month=form.month.data
        ).first()
        if existing_budget and existing_budget.id != budget.id:
            flash('A budget for this category and month already exists.')
            return redirect(url_for('main.edit_budget', budget_id=budget.id))
        
        budget.amount = form.amount.data
        budget.month = form.month.data
        budget.category_id = form.category.data
        try:
            db.session.commit()
            flash('Budget updated successfully.')
            return redirect(url_for('main.view_budgets'))
        except IntegrityError:
            db.session.rollback()
            flash('A budget for this category and month already exists.')
    return render_template('edit_budget.html', title='Edit Budget', form=form, budget=budget)

@main.route('/delete_budget/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.user_id != current_user.id:
        flash('You do not have permission to delete this budget.')
        return redirect(url_for('main.view_budgets'))
    db.session.delete(budget)
    db.session.commit()
    flash('Budget deleted successfully.')
    return redirect(url_for('main.view_budgets'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit()
            flash('Your profile has been updated.', 'success')
            return redirect(url_for('main.profile'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists.', 'danger')
    return render_template('profile.html', title='Profile', form=form)

@main.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('main.change_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('main.profile'))
    return render_template('change_password.html', title='Change Password', form=form)

@main.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.user_id != current_user.id:
        abort(403)  

    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        try:
            db.session.commit()
            flash('Category updated successfully.', 'success')
            return redirect(url_for('main.categories'))
        except IntegrityError:
            db.session.rollback()
            flash('Category name already exists.', 'danger')
    return render_template('edit_category.html', form=form, title='Edit Category')

@main.route('/delete_category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.user_id != current_user.id:
        abort(403)  

    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.', 'success')
    return redirect(url_for('main.categories'))