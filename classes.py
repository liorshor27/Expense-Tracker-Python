import psycopg2
import os
from dotenv import load_dotenv, find_dotenv # Load database credentials from environment variables.

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
        Establishes and returns a new connection to the PostgreSQL database.
        Returns:
            psycopg2.extensions.connection: The database connection object.
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
                date VARCHAR(20),
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
        Replaces the old 'load_from_file' CSV method.
        """
        self.expenses = []
        conn = self.get_connection()
        cur = conn.cursor()
        
        # Select all columns including the unique ID
        cur.execute("SELECT date, category, name, amount, id FROM expenses")
        rows = cur.fetchall()
        
        for row in rows:
            # row structure: (date, category, name, amount, id)
            new_expense = Expense(row[0], row[1], row[2], float(row[3]), row[4])
            self.expenses.append(new_expense)
            
        cur.close()
        conn.close()

    def add_expense(self, expense):
        """
        Adds a new expense object to the database and the internal list.
        Args:
            expense (Expense): The expense object to add.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        
        # Insert into DB and return the generated ID
        cur.execute("""
            INSERT INTO expenses (date, category, name, amount)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """, (expense.date, expense.category, expense.name, expense.amount))
        
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
        Args:
            expense_index (int): The 0-based index of the item to remove.
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

    def save_to_file(self):
        # Deprecated. Kept for backward compatibility with CLI.
        print("Data is automatically saved to the Database.")

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