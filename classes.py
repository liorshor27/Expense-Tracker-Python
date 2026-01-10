import csv
import os
class ExpenseManager:
    """
    Manages the collection of expenses.
    Handles Business Logic: Adding, Deleting, Saving, Loading, and Reporting.
    """
    def __init__(self):
        self.expenses = []  #In-memory list of Expense objects
        self.filename = "my_expenses.csv" #The name of the file where data is saved 
        self.budget_filename = "budget.txt" #The name of the file where budget is saved
        self.load_from_file() #Load data immediately upon instantiation

    def add_expense(self, expense):
        #Adds a new expense object to the internal list
        self.expenses.append(expense)
        print("\nExpense added to memory!\n")

    def delete_expense(self, expense_index):
        """
        Removes an expense from the list based on its index.
        Args:
            expense_index (int): The 0-based index of the item to remove.
        """
        if 0 <= expense_index < len(self.expenses): #Checks if the index is valid
            removed_item = self.expenses.pop(expense_index)
            print(f"Deleted: {removed_item.name} from memory!") 
        else:
            print("Error: Invalid expense number.")
            return False

    def save_to_file(self):
        """
        Saves the current list of expenses to the CSV file (Overwrites).
        """ 
        with open(self.filename, 'w', newline='', encoding='utf-8') as f: 
            writer = csv.writer(f) # Create a writer object

            writer.writerow(["Date", "Category", "Name", "Amount"]) # Write the header row
            
            for exp in self.expenses: # Loop through every expense object
                writer.writerow(exp.to_list()) # Convert to list and write
        
        print(f"Saved {len(self.expenses)} expenses to {self.filename}")

    def load_from_file(self):
        """
        Reads the CSV file and converts each line back into an Expense object.
        """
        if not os.path.exists(self.filename):
            return #File doesn't exist yet (first run)

        with open(self.filename, 'r', encoding='utf-8') as f: 
            reader = csv.reader(f) 
            
            next(reader, None) # Skip the header row

            for row in reader:
                if len(row) >= 4: #Ensure the row has enough columns before parsing
                    date = row[0]
                    category = row[1]
                    name = row[2]
                    amount = row[3]
                    
                    loaded_expense = Expense(date, category, name, amount)
                    self.expenses.append(loaded_expense)
            
            print(f"Loaded {len(self.expenses)} expenses from file.")

    def print_all_expenses(self):
        """Prints a numbered list of all expenses and the total sum."""
        print("\n--- All Expenses ---")
        total = 0  
        i = 1
        
        for exp in self.expenses:
            print(f"{i}. {exp}")
            try: # Try to cast the amount to float, then add to total
                total += float(exp.amount) 
            except ValueError: 
                pass #Ignore invalid amounts
            
            i += 1
            
        print("-" * 20) 
        print(f"Total Spent: {total} NIS") 
        print("-" * 20+"\n")

    def print_report_by_category(self):
        """Aggregates expenses by category and prints a summary."""
        print("\n--- Expenses by Category ---")
        totals = {} #Dictionary to store total per category

        for exp in self.expenses:
            cat = exp.category
            try:
                amt = float(exp.amount)
            except ValueError:
                continue
            
            #If category exists, add to it; otherwise, initialize it.
            if cat in totals:
                totals[cat] += amt
            else:
                totals[cat] = amt

        #Iterate over the dictionary and display results
        for cat, amount in totals.items():
            print(f"{cat}: {amount} NIS")
        print("-" * 20+"\n")

    # --- Budget Management Methods ---
    def set_budget(self, amount):
        """Saves the budget amount to a text file."""
        with open(self.budget_filename, 'w') as f:
            f.write(str(amount))

    def get_budget(self):
        """Loads the budget from file. Returns 0 if not set."""
        if not os.path.exists(self.budget_filename):
            return 0.0
        try:
            with open(self.budget_filename, 'r') as f:
                return float(f.read())
        except ValueError:
            return 0.0

class Expense:
    """
    Represents a single expense record (Data Model).
    Attributes:
        date (str): The date of the expense.
        category (str): The category (e.g., Food, Transport).
        name (str): A description of the expense.
        amount (str): The cost.
    """
    def __init__(self, date, category, name, amount): 
        self.date = date
        self.category = category
        self.name = name
        self.amount = amount

    def to_list(self):
        #Converts the object attributes into a list for CSV storage.
        return [self.date, self.category, self.name, self.amount]

    def __str__(self):
        #Returns a formatted string representation of the expense.
        return f"{self.date} | [{self.category}] {self.name}: {self.amount} NIS"