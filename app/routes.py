# from flask import render_template
# from app import app
# import os

# @app.route('/')
# def index():
#     try:
#         debug_info = {
#             "Working directory": os.getcwd(),
#             "Template folder exists": os.path.exists('templates'),
#             "Template path": os.path.abspath('templates'),
#             "Index exists": os.path.exists('templates/index.html')
#         }
#         print(debug_info)  # This will show in your console
#         return render_template('index.html')
#     except Exception as e:
#         return f"Error: {str(e)}\nDebug info: {debug_info}"

# @app.route('/test')
# def test():
#     return 'This is a test route.'

from flask import render_template
from app import app
from app.models import User, Transaction

@app.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)
