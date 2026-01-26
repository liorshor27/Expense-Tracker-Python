from datetime import datetime

def get_available_months(expenses):
    """
    Scans all expenses to find unique months.
    Handles both string dates and datetime objects robustly.
    """
    available_months = set()
    today = datetime.today()
    
    current_month_str = today.strftime('%m/%Y')
    available_months.add(current_month_str)

    for exp in expenses:
        if not exp.date: 
            continue
        try:
            if isinstance(exp.date, str):
                dt = datetime.strptime(exp.date, "%d/%m/%Y")
            else:
                dt = exp.date
            available_months.add(dt.strftime('%m/%Y'))
        except ValueError:
            pass
    
    sorted_months = sorted(list(available_months), key=lambda x: datetime.strptime(x, "%m/%Y"), reverse=True)
    return sorted_months

def filter_expenses_by_period(expenses, selected_period):
    """
    Filters the expense list based on the user's selection.
    """
    filtered_expenses = []
    target_month = None

    current_month_str = datetime.today().strftime('%m/%Y')

    if selected_period == "Current Month":
        target_month = current_month_str
    elif selected_period == "All History":
        target_month = None
    else:
        target_month = selected_period

    for exp in expenses:
        if not target_month:
            filtered_expenses.append(exp)
            continue
        try:
            if isinstance(exp.date, str):
                exp_dt = datetime.strptime(exp.date, "%d/%m/%Y")
            else:
                exp_dt = exp.date
                
            if exp_dt.strftime('%m/%Y') == target_month:
                filtered_expenses.append(exp)
        except ValueError:
            pass
        
    return filtered_expenses, target_month
                

