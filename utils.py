from datetime import datetime

def get_available_months(expenses):
    """
    Extracts unique months from the expense list for the filter dropdown.
    Refactored: Handles datetime.date objects directly from DB.
    """
    unique_months = set()
    
    for exp in expenses:
        if exp.date:
            month_str = exp.date.strftime("%B %Y") # Example: "January 2026"
            unique_months.add(month_str)
            
    # Sort the months properly (converting back to date for sorting)
    return sorted(list(unique_months), key=lambda x: datetime.strptime(x, "%B %Y"), reverse=True)

def filter_expenses_by_period(expenses, selected_period):
    """
    Filters the expense list based on the user's selection.
    Refactored: Compares date objects directly.
    """
    if selected_period == "All History":
        return expenses, "All History"
        
    filtered_list = []
    
    # Logic for "Current Month" or specific "Month Year" selection
    target_month_str = selected_period
    
    if selected_period == "Current Month":
        target_month_str = datetime.now().strftime("%B %Y")

    for exp in expenses:
        if exp.date:
            # Check if the expense's month matches the target
            if exp.date.strftime("%B %Y") == target_month_str:
                filtered_list.append(exp)
                
    return filtered_list, target_month_str

