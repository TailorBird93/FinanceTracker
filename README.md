# Personal Finance Tracker

## Project Overview

The **Personal Finance Tracker** is a web application designed to help users manage their personal finances by tracking income, expenses, budgets, and financial goals. It offers a user-friendly interface for recording transactions, categorizing expenses, and monitoring financial health over time.

## Features

- **User Authentication**
  - Secure user registration and login functionalities.
  - Only authenticated users can manage their financial data.
  
- **Transaction Management**
  - Full CRUD (Create, Read, Update, Delete) operations for transactions.
  - Transactions are organized into customizable categories.
  - Confirmation prompts before deleting transactions to prevent accidental loss.
  
- **Category Management**
  - Users can create, edit, and delete categories to organize their transactions.
  - Ensures that categories are unique per user.
  
- **Budgeting**
  - Set monthly budgets for different categories.
  - Monitor spending against set budgets.
  
- **Responsive Design**
  - Accessible on all device sizes using Bootstrap for a consistent look and feel.
  
- **Security Features**
  - CSRF protection for all forms.
  - Authorization checks to ensure users can only modify their own data.

## Technologies Used

- **Backend**:
  - Python 3.12
  - Flask
  - Flask-Login
  - Flask-Bootstrap
  - Flask-Migrate
  - SQLAlchemy

- **Frontend**:
  - Bootstrap 5
  - HTML5
  - CSS3
  - JavaScript

- **Database**:
  - SQLite (for development)
  - PostgreSQL (for production on Heroku)

- **Deployment**:
  - Heroku
  - Gunicorn

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for version control)
- Heroku CLI (for deployment)

### Installation

1. **Clone the Repository** (if using version control):

    ```bash
    git clone <repository-url>
    cd finance_tracker
    ```

2. **Create and Activate a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**:

    ```bash
    python app.py
    ```

    Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to see the application running.

## Database Setup

The application uses SQLite for development purposes and PostgreSQL for production.

### Creating the Development Database

1. **Set the FLASK_APP Environment Variable**:

    - On macOS/Linux:

        ```bash
        export FLASK_APP=manage.py
        ```

    - On Windows:

        ```bash
        set FLASK_APP=manage.py
        ```

2. **Create the Database Tables**:

    ```bash
    flask shell
    ```

3. **In the Shell, Run**:

    ```python
    from app import db
    db.create_all()
    exit()
    ```

## User Authentication

The application includes secure user registration and login functionalities.

### Features

- **Register**: Create a new user account.
- **Login**: Access your personal dashboard.
- **Logout**: Securely log out of your account.
- **Access Control**: Only authenticated users can manage transactions and categories.

### How to Use

1. **Registering a New Account**:

    - Navigate to the **"Register"** page.
    - Fill out the registration form with a username, email, and password.
    - Submit the form to create your account.

2. **Logging In**:

    - Navigate to the **"Login"** page.
    - Enter your registered email and password.
    - Submit the form to access your dashboard.

3. **Logging Out**:

    - Click on the **"Logout"** button in the navigation menu to end your session.

## Transaction Management

The application supports full CRUD operations for transactions:

- **Create**: Add new transactions.
- **Read**: View a list of your transactions.
- **Update**: Edit existing transactions.
- **Delete**: Delete transactions.

### Features

- Transactions are displayed in a table with date, category, amount, and description.
- Users can only edit or delete their own transactions.
- Confirmation prompts are provided before deleting a transaction.

### How to Use

1. **Adding a Transaction**:

    - Navigate to **"Add Transaction"** in the navigation menu.
    - Fill out the form and submit.

2. **Editing a Transaction**:

    - On the transactions page, click **"Edit"** next to the transaction you wish to modify.
    - Update the details and submit.

3. **Deleting a Transaction**:

    - On the transactions page, click **"Delete"** next to the transaction you wish to remove.
    - Confirm the deletion when prompted.

## Category Management

Organize your transactions into customizable categories for better financial tracking.

### Features

- **Create**: Add new categories.
- **Read**: View a list of your categories.
- **Update**: Edit existing categories.
- **Delete**: Delete categories.

### How to Use

1. **Adding a Category**:

    - Navigate to **"Add Category"** in the navigation menu.
    - Enter the category name and submit.

2. **Editing a Category**:

    - On the categories page, click **"Edit"** next to the category you wish to modify.
    - Update the category name and submit.

3. **Deleting a Category**:

    - On the categories page, click **"Delete"** next to the category you wish to remove.
    - Confirm the deletion when prompted.

## Security Features

- **User Authentication**: Only logged-in users can manage transactions and categories.
- **Authorization Checks**: Users cannot edit or delete transactions or categories that do not belong to them.
- **CSRF Protection**: All forms include CSRF tokens to protect against cross-site request forgery attacks.
- **Input Validation**: Forms validate user input to ensure data integrity and security.

## Deployment to Heroku

Deploy your application to Heroku to make it accessible online.

### Prerequisites

- Heroku account
- Heroku CLI installed

### Deployment Steps

1. **Login to Heroku**:

    ```bash
    heroku login
    ```

2. **Create a Heroku App**:

    ```bash
    heroku create your-app-name
    ```

    Replace `your-app-name` with a unique name. If omitted, Heroku will generate one.

3. **Add PostgreSQL Add-on** (if using a database):

    ```bash
    heroku addons:create heroku-postgresql:hobby-dev
    ```

4. **Set Environment Variables**:

    ```bash
    heroku config:set SECRET_KEY='your-secret-key'
    ```

    Replace `'your-secret-key'` with a strong secret key.

5. **Prepare for Deployment**:

    - **Create `Procfile`**:

        ```plaintext
        web: gunicorn app:create_app()
        ```

    - **Specify Python Version** in `runtime.txt`:

        ```plaintext
        python-3.12.0
        ```

        Ensure the version is supported by Heroku. Refer to [Heroku Python Support](https://devcenter.heroku.com/articles/python-support#supported-runtimes) for the latest versions.

6. **Install Gunicorn and Update `requirements.txt`**:

    ```bash
    pip install gunicorn
    pip freeze > requirements.txt
    ```

7. **Commit Changes**:

    ```bash
    git add .
    git commit -m "Prepare for Heroku deployment"
    ```

8. **Deploy to Heroku**:

    ```bash
    git push heroku main
    ```

    *(Replace `main` with your branch name if different.)*

9. **Run Database Migrations**:

    ```bash
    heroku run flask db upgrade
    ```

10. **Open Your App**:

    ```bash
    heroku open
    ```

### Troubleshooting Deployment Issues

- **Check Logs**:

    ```bash
    heroku logs --tail
    ```

- **Ensure All Dependencies Are Listed** in `requirements.txt`.

- **Verify `Procfile` and `runtime.txt`** are correctly formatted and placed in the root directory.




## Additional Sections 

### Wireframes


```markdown

