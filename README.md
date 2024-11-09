# Personal Finance Tracker

## Project Overview

The Personal Finance Tracker is a web application designed to help users manage their personal finances by tracking income, expenses, budgets, and financial goals.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the Repository** (if using version control):

   ```bash
   git clone <repository-url>
   cd finance_tracker
2. **Create and Activate a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  (On Windows use `venv\Scripts\activate`)
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
4. **Run the application**:
    ```bash
    python app.py
    Open your web browser and go to
    http://127.0.0.1:5000/ to see the application running.

### Technologies Used
Python 3
Flask

## Database Setup

The application uses SQLite for development purposes.

### Creating the Database

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
3. **In the shell, run:**

    ```bash 
    db.create_all()
    exit()

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

   - Navigate to "Add Transaction" in the navigation menu.
   - Fill out the form and submit.

2. **Editing a Transaction**:

   - On the home page, click "Edit" next to the transaction you wish to modify.
   - Update the details and submit.

3. **Deleting a Transaction**:

   - On the home page, click "Delete" next to the transaction you wish to remove.
   - Confirm the deletion when prompted.

## Security Features

- **User Authentication**: Only logged-in users can manage transactions.
- **Authorization Checks**: Users cannot edit or delete transactions that do not belong to them.
- **CSRF Protection**: All forms include CSRF tokens to protect against cross-site request forgery attacks.
