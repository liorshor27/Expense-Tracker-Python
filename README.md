# Personal Expense Tracker

Expense tracking app I built to practice full-stack development. Started as a simple CSV script, then migrated to PostgreSQL for better data handling.

Has both a web dashboard (Streamlit) and a CLI for quick terminal access.

## Features

* PostgreSQL database (moved from CSV)
* Environment variables for DB credentials (no hardcoded passwords)
* Web dashboard with month filtering and category breakdowns
* Spending analysis comparing current month vs historical average
* Full CRUD operations

## Tech Stack

* Python 3.10+
* Streamlit for the web UI
* Plotly for charts
* PostgreSQL
* psycopg2, python-dotenv

## Project Structure

* `app.py` - Streamlit web app
* `classes.py` - ExpenseManager class, handles DB connections and CRUD
* `main.py` - CLI interface
* `utils.py` - Helper functions for filtering and analysis
* `charts.py` - Plotly chart generation

## Setup

1. Clone the repo:
```bash
git clone https://github.com/liorshor27/Expense-Tracker-Python.git
cd Expense-Tracker-Python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL:
   - Make sure PostgreSQL is running
   - Create a database called `expenses_db`
   - Create a `.env` file in the project root:
     ```env
     DB_HOST=localhost
     DB_NAME=expenses_db
     DB_USER=postgres
     DB_PASS=your_password
     ```

4. Tables are created automatically when you first run the app (ExpenseManager handles it).

## Usage

Run the web dashboard:
```bash
streamlit run app.py