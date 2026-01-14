import streamlit as st
from classes import ExpenseManager, Expense
from datetime import datetime 
from styles import load_css
from charts import create_expense_pie_chart
from utils import get_available_months, filter_expenses_by_period, analyze_spending_trends

#Load custom CSS styles  
load_css()

# --- Page Setup ---
st.title("💰 My Expense Tracker")

# --- Session State Initialization ---
# Streamlit reruns the entire script upon every interaction (button click, input change).
# We use 'st.session_state' to persist the ExpenseManager object across these reruns.
# Without this, the manager would reset to empty every time the user clicks a button.

if 'manager' not in st.session_state:
    st.session_state.manager = ExpenseManager()

#Create a local reference for easier access
manager = st.session_state.manager

# --- Sidebar: Add New Expense ---
st.sidebar.header("Add New Expense")

#User Inputs
#We default the date to today
input_date = st.sidebar.date_input("Date", datetime.today())
#Convert date object to string format (DD/MM/YYYY) for storage
date_str = input_date.strftime("%d/%m/%Y")

categories = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"]
input_category = st.sidebar.selectbox("Category", categories)

#Logic for Adding Expense
input_name = st.sidebar.text_input("Description")
input_amount = st.sidebar.number_input("Amount", min_value=0.0, step=1.0)

if st.sidebar.button("Add Expense"):
    #Simple validation: Ensure name is not empty and amount is positive
    if input_name and input_amount > 0:
        #Create a new Expense object
        new_expense = Expense(date_str, input_category, input_name, str(input_amount))
        manager.add_expense(new_expense)

        #Add to manager and save immediately to CSV
        manager.save_to_file()

        st.sidebar.success("Added successfully!")
    else:
        st.sidebar.error("Please fill all fields correctly.")

# --- Sidebar: Budget Management ---
st.sidebar.markdown("---")
st.sidebar.header("💳 Monthly Budget")

#Load current budget
current_budget = manager.get_budget()
#Update budget
new_budget = st.sidebar.number_input("Set Budget (NIS)", value=current_budget, min_value=0.0, step=100.0)

if st.sidebar.button("Update Budget"):
    manager.set_budget(new_budget)
    st.sidebar.success("Budget Updated!")
    st.rerun()

# --- Time Filter ---
st.sidebar.markdown("---")
st.sidebar.header("📅 Time Filter")

#Dynamic Month Loading:
#Fetch available months from utils to populate the dropdown
sorted_months = get_available_months(manager.expenses)
filter_options = ["Current Month"] + sorted_months + ["All History"]

selected_period = st.sidebar.selectbox("Select Period", filter_options, index=0)

# --- Sidebar: SaaS Analysis ---
st.sidebar.markdown("---")
if st.sidebar.button("📊 Run Analysis"):
    #Perform trend analysis using utils
    curr, avg, is_high = analyze_spending_trends(manager.expenses,selected_period)
    
    if avg > 0:
        if is_high:
            st.sidebar.error(f"⚠️ High Spending! You passed your average of {avg:.0f} NIS.")
        else:
            st.sidebar.success(f"✅ Good Job! You are below your average of {avg:.0f} NIS.")
    else:
        st.sidebar.info("Not enough data history to calculate trends yet.")


# --- Main Display Area ---

#Create two tabs: one for the raw list, one for analytics
tab1, tab2 = st.tabs(["📋 List", "📊 Report"])

#Filter Logic:
#Delegate filtering responsibility to utils function
filtered_expenses, target_month_str = filter_expenses_by_period(manager.expenses, selected_period)

#Get today's date for filtering
today = datetime.today()
with tab1:
    # --- Tab 1: Expense List & Management ---
    st.subheader("All Expenses")
    
    #Check if there are expenses to display
    if manager.expenses:
        #Convert Expense objects to a list of dictionaries.
        #Streamlit requires this format to render tables.
        data = []
        i=1
        for exp in manager.expenses:
            data.append({"Number": i, "Date": exp.date, "Category": exp.category, "Name": exp.name, "Amount": f"{exp.amount} NIS"})
            i+=1
        
        #Render the static table
        st.table(data)
        
        # --- Deletion Section ---
        st.divider()
        st.write("### Delete Expense")

        #Numeric input for selecting the item index
        del_num = st.number_input("Enter line number to delete", min_value=1, step=1)
        if st.button("Delete"):
            #Convert user-friendly index (1-based) to list index (0-based)
            manager.delete_expense(del_num - 1)

            #Save changes to file
            manager.save_to_file()

            #Rerun the app to refresh the table immediately
            st.rerun() 
    else:
        st.info("No expenses yet. Add one from the sidebar!")

with tab2:
    # --- Tab 2: Analytics & Reports ---
    st.subheader(f"Overview for {today.strftime('%B %Y')}") 
    
    #1. Filter data for the current month only
    current_month_total = 0
    category_totals = {}
    
    #Aggregate expenses by category using a dictionary
    totals = {}
    for exp in manager.expenses:
        try:
            #Parse date to check month/year
            exp_date_obj = datetime.strptime(exp.date, "%d/%m/%Y")
            
            #Check if expense belongs to current month/year
            if exp_date_obj.month == today.month and exp_date_obj.year == today.year:
                amt = float(exp.amount)
                current_month_total += amt
                category_totals[exp.category] = category_totals.get(exp.category, 0) + amt
        except ValueError:
            pass

    #2. Calculate remaining budget
    budget = manager.get_budget()
    remaining = budget - current_month_total
    
    #3. Display Metrics (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Budget", f"{budget:,.0f} ₪")
    col2.metric("Total Spent", f"{current_month_total:,.0f} ₪", delta=f"-{current_month_total} this month", delta_color="inverse")
    
    #Dynamic coloring: Red if over budget, Green if safe
    col3.metric("Remaining", f"{remaining:,.0f} ₪", delta=f"{remaining}", delta_color="normal" if remaining >= 0 else "inverse")

    st.divider()

    # 4. Display Pie Chart
    if category_totals:
        #Generate the chart object using the helper function from charts.py
        fig = create_expense_pie_chart(category_totals)
        
        #Render the chart in Streamlit 
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("No expenses recorded for this month yet.")
