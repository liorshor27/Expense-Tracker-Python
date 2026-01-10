from datetime import datetime

def get_available_months(expenses):
    """
    Scans all expenses to find unique months (MM/YYYY).
    Returns a sorted list of months (newest first).
    """
    available_months = set()
    today = datetime.today()
    current_month_str = today.strftime('%m/%Y')

    #Always add current month
    available_months.add(current_month_str)

    for exp in expenses:
        try:
            dt = datetime.strptime(exp.date, "%d/%m/%Y")
            month_str = dt.strftime('%m/%Y')
            available_months.add(month_str)
        except ValueError:
            pass

    #Sort: Convert to datetime for sorting, then back to string
    sorted_months = sorted(list(available_months), key=lambda x: datetime.strptime(x, "%m/%Y"), reverse=True)
    return sorted_months

def filter_expenses_by_period(expenses, selected_period):
    """
    Filters the expense list based on the user's selection.
    Returns:
        - filtered_list: List of Expense objects
        - target_month: The specific month string (e.g., "01/2026") or None if "All History".
    """
    filtered_expenses = []
    target_month = None
    
    current_month_str = datetime.today().strftime('%m/%Y')

    #Determine the target month based on selection
    if selected_period == "Current Month":
        target_month = current_month_str
    elif selected_period == "All History":
        target_month = None
    else:
        target_month = selected_period

    #Perform the filtering
    for exp in expenses:
        if target_month:
            try:
                exp_dt = datetime.strptime(exp.date, "%d/%m/%Y")
                if exp_dt.strftime('%m/%Y') == target_month:
                    filtered_expenses.append(exp)
            except ValueError:
                pass
        else:
            #"All History" - include everything
            filtered_expenses.append(exp)
            
    return filtered_expenses, target_month

def analyze_spending_trends(expenses):
    """
    Calculates current month spending vs. historical average.
    Returns:
        - current_spent (float)
        - avg_spent (float)
        - is_high (bool): True if spending is above average
    """
    today = datetime.today()
    current_month_str = today.strftime('%m/%Y')
    
    monthly_sums = {}
    
    #Aggregate spending by month
    for exp in expenses:
        try:
            dt = datetime.strptime(exp.date, "%d/%m/%Y")
            m_str = dt.strftime('%m/%Y')
            monthly_sums[m_str] = monthly_sums.get(m_str, 0) + float(exp.amount)
        except ValueError:
            pass
            
    current_spent = monthly_sums.get(current_month_str, 0)
    
    #Calculate average of PAST months only
    past_months = [val for key, val in monthly_sums.items() if key != current_month_str]
    
    avg_spent = 0
    if past_months:
        avg_spent = sum(past_months) / len(past_months)
        
    is_high = current_spent > avg_spent and avg_spent > 0
    
    return current_spent, avg_spent, is_high