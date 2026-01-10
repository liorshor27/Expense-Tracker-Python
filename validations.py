from datetime import datetime

# Constant list of allowed categories. 
# Using a predefined list prevents typos (e.g., "Food" vs "food").

CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"]

def get_valid_category():
    """
    Displays the list of categories and prompts the user to select one by index.
    Returns:
        str: The name of the selected category.
    """
    print("\n--- Select Category ---")
    i=1
    for cat in CATEGORIES:
        print(f"{i}. {cat}")
        i+=1
    
    while True:
        choice = input("Enter category number: ")
        
        #Validate that the input is a digit and within the valid range
        if choice.isdigit(): 
            idx = int(choice) - 1 #Ajust the users choise to an array that starts at index 0
            if 0 <= idx < len(CATEGORIES):
                return CATEGORIES[idx] #Return catgory name string
        else:
            print("Invalid choice. Please choose a number from the list.")

def get_valid_amount():
    """
    Prompts the user for an amount and validates that it is a positive number.
    Returns:
        str: The valid amount as a string (to be stored in CSV).
    """
    while True:
        amount_str = input("Amount: ")
        #Try converting the string to a float
        try:
            amount = float(amount_str) 
            if amount > 0:
                return amount_str # Return as a string
            else: 
                print("Amount must be positive.")

        # Handle cases where input is not a number (e.g., "abc")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_valid_date():
    """
    Prompts the user for a date and validates the format (DD/MM/YYYY).
    Returns:
        str: The valid date string.
    """
    while True:
        date_str = input("Date (DD/MM/YYYY): ")
        try:
            #parsing the date to check if it matches the required format
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except ValueError:
            print("Invalid format. Please use DD/MM/YYYY (e.g., 01/01/2026)")