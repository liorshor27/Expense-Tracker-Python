# 💰 Personal Expense Tracker

A smart expense tracking application designed to help manage monthly budgets effectively.

I built this project to simulate a real-world **Full-Stack development process**. It started as a simple script using CSV files, and I later refactored it to work with a **PostgreSQL database** to implement proper data management and security practices.

The app features a **Web Dashboard** (Streamlit) for visualization and a **CLI** tool for quick updates.

## 🚀 Features

* **SQL Database:** Transferred data storage from CSV to **PostgreSQL** to handle queries efficiently and support more data.
* **Security Best Practices:** Database credentials are managed via **Environment Variables** (`.env`) to prevent exposing sensitive data in the code.
* **Interactive Dashboard:** A user-friendly interface to filter expenses by month, view breakdowns by category (Pie Charts), and track budget goals.
* **Smart Analytics:**
    * Calculates spending trends (comparing current month vs. average).
    * Uses SQL aggregations for faster performance.
* **CRUD Operations:** Full ability to Add, View, Delete, and Update expenses directly in the DB.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Frontend:** Streamlit, Plotly (for charts)
* **Database:** PostgreSQL
* **Libraries:** `psycopg2` (SQL Adapter), `python-dotenv`

## 📂 Project Structure

* `app.py` - Main Web Application file (UI & State).
* `classes.py` - Contains the `ExpenseManager` class (Backend logic & SQL connection).
* `main.py` - Command Line Interface (CLI) for terminal usage.
* `utils.py` - Helper functions for data parsing and trend analysis.
* `charts.py` - Generates the Plotly graphs.
* `init_db.py` - One-time script to initialize the database tables.

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/liorshor27/Expense-Tracker-Python.git](https://github.com/liorshor27/Expense-Tracker-Python.git)
    cd Expense-Tracker-Python
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Configuration:**
    * Make sure you have PostgreSQL installed.
    * Create a database named `expenses_db`.
    * Create a `.env` file in the root folder and add your local DB credentials:
        ```env
        DB_HOST=localhost
        DB_NAME=expenses_db
        DB_USER=postgres
        DB_PASS=your_password
        ```

4.  **Initialize Tables:**
    Run this script once to set up the tables:
    ```bash
    python init_db.py
    ```

## ▶️ Usage

**To run the Web Dashboard:**
```bash
streamlit run app.py