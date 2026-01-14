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

from datetime import datetime

from datetime import datetime

def analyze_spending_trends(expenses, selected_month_str=None):
    """
    Analyzes spending trends by comparing a specific month's spending
    against the average of strictly previous months.

    Args:
        expenses (list): A list of Expense objects containing date and amount.
        selected_month_str (str, optional): The target month in 'MM/YYYY' format.
                                            If None or 'All History', defaults to current date.

    Returns:
        tuple: A tuple containing:
            - current_spent (float): Total spending for the target month.
            - avg_spent (float): Average spending of all previous months.
            - is_high (bool): True if current spending exceeds average by >10%.
    """
    
    # 1. Determine the target month for analysis
    if selected_month_str and selected_month_str != "All History":
        try:
            # Parse the selected month from the dropdown (MM/YYYY)
            month, year = selected_month_str.split("/")
            current_month_dt = datetime(int(year), int(month), 1)
        except ValueError:
            # Fallback to today if parsing fails
            today = datetime.today()
            current_month_dt = datetime(today.year, today.month, 1)
    else:
        # Default to current real-world date
        today = datetime.today()
        current_month_dt = datetime(today.year, today.month, 1)

    monthly_sums = {}

    # 2. Aggregate expenses by month (Robust date parsing)
    for exp in expenses:
        if not exp.date: 
            continue
        
        dt_obj = None
        date_str = str(exp.date).strip()
        
        # Try parsing multiple date formats to ensure data integrity
        # Supports: DD/MM/YYYY (IL/EU), YYYY-MM-DD (ISO/DB), MM/DD/YYYY (US)
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
            try:
                dt_obj = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        
        if dt_obj:
            # Normalize to the first day of the month for grouping
            month_key = datetime(dt_obj.year, dt_obj.month, 1)
            try:
                monthly_sums[month_key] = monthly_sums.get(month_key, 0) + float(exp.amount)
            except ValueError:
                pass # Skip invalid amounts

    # 3. Calculate Metrics
    current_spent = monthly_sums.get(current_month_dt, 0)

    # Filter: Include only months strictly BEFORE the target month
    # This prevents future months or the current month from skewing the average
    past_values = [
        amount for m, amount in monthly_sums.items()
        if m < current_month_dt
    ]

    # Calculate historical average
    avg_spent = 0
    if past_values:
        avg_spent = sum(past_values) / len(past_values)
    
    # 4. Determine Status (High spending flag)
    # Threshold includes a 10% buffer to avoid false alarms on minor deviations
    is_high = current_spent > avg_spent * 1.1 if avg_spent > 0 else False

    return current_spent, avg_spent, is_high