#Import classes and validation functions from other modules
from classes import ExpenseManager, Expense
from validations import get_valid_date, get_valid_amount, get_valid_category

def main():
    """Main execution function handling the user menu loop."""
    manager = ExpenseManager() 
    
    while True: 
        print("1. Add Expense")
        print("2. Show Expenses")
        print("3. Show Report (By Category)")
        print("4. Delete Expense")
        print("5. Set Monthly Budget")
        print("6. Save & Exit")

        choice = input("Select option: ")

        if choice == "1":
            #Collect validated input from the user
            d = get_valid_date() 
            c = get_valid_category() 
            n = input("Name: ")
            a = get_valid_amount() 
            
            #Create a new Expense object and add it to the manager
            manager.add_expense(Expense(d, c, n, a))
        
        elif choice == "2":
            manager.print_all_expenses()

        elif choice == "3":
            manager.print_report_by_category()
            budget = manager.get_budget()
            if budget > 0:
                total_spent = sum(float(exp.amount) for exp in manager.expenses)
                remaining = budget - total_spent
                
                print(f"--- Budget Status ---")
                print(f"Monthly Budget: {budget} NIS")
                print(f"Total Spent:    {total_spent} NIS")
                print(f"Remaining:      {remaining} NIS")
                print("-" * 20 + "\n")
            else:
                print("(No budget set for this month)\n")

        elif choice == "4":
            manager.print_all_expenses() 
            user_input = input("Enter the number to delete: ") 
            
            if user_input.isdigit():
                #Convert 1-based user index to 0-based list index
                expense_num = int(user_input) 
                manager.delete_expense(expense_num - 1)
            else:
                print("Invalid input, please enter a number.")
            
        elif choice == "5":
            print("\n--- Set Monthly Budget ---")
            amount_str = get_valid_amount()
            manager.set_budget(float(amount_str))
            print("Budget updated successfully!")
            
        elif choice == "6":
            manager.save_to_file()
            print("Goodbye!")
            break 
        else:
            print("Invalid option, try again.")

if __name__ == "__main__": 
    main()