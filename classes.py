import psycopg2
import os
from dotenv import load_dotenv, find_dotenv # Load database credentials from environment variables.
from datetime import datetime

load_dotenv(find_dotenv())

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "expenses_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS") 

if not DB_PASS:
    raise ValueError("Database password not found. Please set DB_PASS in your .env file.")
class ExpenseManager:
    # Manages expense CRUD operations against the PostgreSQL database. 

    def __init__(self):
        self.expenses = []  # In-memory list of Expense objects
        
        # Initialize Database Tables
        self.create_tables()
        
        # Load data immediately upon instantiation from the Database
        self.load_from_db()

    def get_connection(self):
        """
        Returns a new database connection.
        """
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )

    def create_tables(self):
        """
        Creates the necessary tables (expenses, budget) in the database if they do not exist.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        
        # Create expenses table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            date DATE,  
            category VARCHAR(50),
            name VARCHAR(100),
            amount NUMERIC
            );
        """)
        
        # Create budget table (single row logic)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS budget (
                id SERIAL PRIMARY KEY,
                amount NUMERIC
            );
        """)
        
        # Initialize budget with 0 if table is empty
        cur.execute("SELECT count(*) FROM budget")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO budget (amount) VALUES (0)")

        conn.commit()
        cur.close()
        conn.close()

    def load_from_db(self):
        """
        Fetches all expenses from the database and populates the in-memory list.
        """
        self.expenses = []
        conn = self.get_connection()
        cur = conn.cursor()
        
        # Select all columns including the unique ID
        cur.execute("SELECT date, category, name, amount, id FROM expenses")
        rows = cur.fetchall()
        
        for row in rows:
            raw_date = row[0]
            if isinstance(raw_date, datetime) or hasattr(raw_date, 'strftime'):
                clean_date = raw_date.strftime("%d/%m/%Y")
            elif isinstance(raw_date, str) and "-" in raw_date:
                try:
                    dt_obj = datetime.strptime(raw_date, "%Y-%m-%d")
                    clean_date = dt_obj.strftime("%d/%m/%Y")
                except ValueError:
                    clean_date = raw_date # Fallback
            else:
                clean_date = str(raw_date)
            new_expense = Expense(clean_date, row[1], row[2], float(row[3]), row[4])
            self.expenses.append(new_expense)
            
            
        cur.close()
        conn.close()

    def add_expense(self, expense):
        """
        Adds an expense to the database and in-memory list.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            dt_obj = datetime.strptime(expense.date, "%d/%m/%Y")
            formatted_date = dt_obj.strftime("%Y-%m-%d")
        except ValueError:
            formatted_date = expense.date

        # Insert into DB and return the generated ID
        cur.execute("""
            INSERT INTO expenses (date, category, name, amount)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (formatted_date, expense.category, expense.name, expense.amount))
        
        new_id = cur.fetchone()[0]
        expense.id = new_id  # Assign the DB ID to the object
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Add to memory
        self.expenses.append(expense)
        print("\nExpense added to Database and memory!\n")

    def delete_expense(self, expense_index):
        """
        Removes an expense from the list and the database based on its list index.
        """
        if 0 <= expense_index < len(self.expenses):
            expense_to_remove = self.expenses[expense_index]
            
            # Delete from Database using the unique ID
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM expenses WHERE id = %s", (expense_to_remove.id,))
            conn.commit()
            cur.close()
            conn.close()
            
            # Remove from memory
            removed_item = self.expenses.pop(expense_index)
            print(f"Deleted: {removed_item.name} from Database and memory!") 
        else:
            print("Error: Invalid expense number.")

    def print_all_expenses(self):
        """
        Prints all expenses currently in memory.
        """
        print("\n--- Expense List ---")
        for i, exp in enumerate(self.expenses):
            print(f"{i + 1}. {exp.date} | {exp.category} | {exp.name} | {exp.amount} NIS")
        print("--------------------\n")

    def print_report_by_category(self):
        """
        Calculates and prints the total expenses grouped by category.
        """
        print("\n--- Expenses by Category ---")
        totals = {}
        for exp in self.expenses:
            # Clean and convert amount to float
            try:
                amount = float(exp.amount)
            except ValueError:
                amount = 0.0
            
            if exp.category in totals:
                totals[exp.category] += amount
            else:
                totals[exp.category] = amount
        
        for cat, amount in totals.items():
            print(f"{cat}: {amount} NIS")
        print("-" * 20 + "\n")

    # Budget Management Methods 

    def set_budget(self, amount):
        """
        Updates the budget amount in the database.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE budget SET amount = %s", (amount,))
        conn.commit()
        cur.close()
        conn.close()

    def get_budget(self):
        """
        Loads the budget from the database. Returns 0 if not set.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT amount FROM budget LIMIT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return float(result[0]) if result else 0.0

    def get_spending_analysis(self):
        """
        Analyzes spending trends by comparing current month's spending against 
        the historical average of all previous months.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        
        # Calculate average monthly spending from all months BEFORE current month
        cur.execute("""
            SELECT AVG(monthly_total)
            FROM (
                SELECT SUM(amount) as monthly_total
                FROM expenses
                WHERE date < DATE_TRUNC('month', CURRENT_DATE)
                GROUP BY DATE_TRUNC('month', date)
            ) sub;
        """)
        avg_result = cur.fetchone()[0]
        average_spending = float(avg_result) if avg_result else 0.0

        # Calculate total spending for the current month
        cur.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE date >= DATE_TRUNC('month', CURRENT_DATE);
        """)
        curr_result = cur.fetchone()[0]
        current_month_total = float(curr_result) if curr_result else 0.0

        cur.close()
        conn.close()

        return current_month_total, average_spending

class Expense:
    """
    Represents a single expense record.
    """
    def __init__(self, date, category, name, amount, id=None): 
        self.id = id
        self.date = date
        self.category = category
        self.name = name
        self.amount = amount