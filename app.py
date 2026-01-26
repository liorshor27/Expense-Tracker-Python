import streamlit as st
from classes import ExpenseManager, Expense
from datetime import datetime
from styles import load_css
from charts import create_expense_pie_chart
from utils import get_available_months, filter_expenses_by_period
from validations import CATEGORIES

# Load custom CSS styles  
load_css()

# Page Setup
st.title("💰 My Expense Tracker")

# Ensure ExpenseManager persists across reruns.
if 'manager' not in st.session_state:
    st.session_state.manager = ExpenseManager()

# Create a local reference for easier access
manager = st.session_state.manager

# Sidebar: Add New Expense
st.sidebar.header("Add New Expense")

# User Inputs
# We default the date to today
input_date = st.sidebar.date_input("Date", datetime.today())

input_category = st.sidebar.selectbox("Category", CATEGORIES)

# Logic for Adding Expense
input_name = st.sidebar.text_input("Description")
input_amount = st.sidebar.number_input("Amount", min_value=0.0, step=1.0)

if st.sidebar.button("Add Expense"):
    # Ensure name is not empty and amount is positive
    if input_name and input_amount > 0:
        # Create a new Expense object and add it once
        new_expense = Expense(input_date, input_category, input_name, str(input_amount))
        manager.add_expense(new_expense)

        st.sidebar.success("Added successfully!")
    else:
        st.sidebar.error("Please fill all fields correctly.")

# Budget Management
st.sidebar.markdown("---")
st.sidebar.header("💳 Monthly Budget")

# Load current budget
current_budget = manager.get_budget()
# Update budget
new_budget = st.sidebar.number_input("Set Budget (NIS)", value=current_budget, min_value=0.0, step=100.0)

if st.sidebar.button("Update Budget"):
    manager.set_budget(new_budget)
    st.sidebar.success("Budget Updated!")
    st.rerun()

# Time Filter
st.sidebar.markdown("---")
st.sidebar.header("📅 Time Filter")

# Dynamic Month Loading:
# Fetch available months from utils to populate the dropdown
sorted_months = get_available_months(manager.expenses)
filter_options = ["Current Month"] + sorted_months + ["All History"]

selected_period = st.sidebar.selectbox("Select Period", filter_options, index=0)

# Analysis
st.sidebar.markdown("---")
if st.sidebar.button("📊 Run Analysis"):
    # Perform trend analysis using utils
    curr, avg = manager.get_spending_analysis(selected_period)
    is_high = curr > avg
    if avg > 0:
        if is_high:
            st.sidebar.error(f"⚠️ High Spending! You passed your average of {avg:,.0f} NIS.")
        else:
            st.sidebar.success(f"✅ Good Job! You are below your average of {avg:,.0f} NIS.")
            # Display current spend context for better UX
            st.sidebar.markdown(f"*(Current: {curr:,.0f} ₪)*") 
    else:
        st.sidebar.info("Insufficient data history for trend analysis.")
    


# Main Display Area
# Create two tabs: one for the raw list, one for analytics
tab1, tab2 = st.tabs(["📋 List", "📊 Report"])

# Filter Logic:
# Delegate filtering responsibility to utils function
filtered_expenses, target_month_str = filter_expenses_by_period(manager.expenses, selected_period)

# Get today's date for filtering
today = datetime.today()
with tab1:
    # Expense List & Management
    if selected_period == "All History":
        st.subheader("All Expenses History")
    else:
        st.subheader(f"Expenses for {target_month_str}")
    
    # Check if there are expenses to display
    if filtered_expenses:
        data = []
        i = 1
        for exp in filtered_expenses:
            date_obj = exp.date  
            data.append({
                "Number": i, 
                "Date": date_obj,  
                "Category": exp.category, 
                "Name": exp.name, 
                "Amount": float(exp.amount) 
            })
            i += 1
        st.dataframe(
            data,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Number": st.column_config.NumberColumn("#", format="%d", width="small"),
                "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"), 
                "Amount": st.column_config.NumberColumn("Amount", format="%.2f ₪"), 
                "Category": st.column_config.TextColumn("Category"),
                "Name": st.column_config.TextColumn("Name")
            }
        )
        
        
        #st.divider()
        st.write("### Delete Expense")
        st.caption("Note: To delete, please ensure you are viewing 'All History' or find the specific expense ID.")

        del_num = st.number_input("Enter line number to delete", min_value=1, step=1)
        if st.button("Delete"):
            if selected_period != "All History":
                st.error("Please switch to 'All History' to delete items by index accurately.")
            else:
                manager.delete_expense(del_num - 1)
                st.rerun() 
    else:
        st.info(f"No expenses found for {selected_period}.")

with tab2:
    # Tab 2: Analytics & Reports
    if selected_period == "All History":
        st.subheader("Overview: All Time History")
    else:
        st.subheader(f"Overview for {target_month_str}")

    period_total = 0
    category_totals = {}

    for exp in filtered_expenses:
        try:
            amt = float(exp.amount)
            period_total += amt
            category_totals[exp.category] = category_totals.get(exp.category, 0) + amt
        except ValueError:
            # Skip invalid amounts to keep the dashboard robust
            continue

    # Calculate remaining budget
    budget = manager.get_budget()

    if selected_period == "All History":
        st.metric("Total Spent (All Time)", f"{period_total:,.0f} ₪")
    else:
        remaining = budget - period_total
    
        # Display Metrics (KPIs)
        col1, col2, col3 = st.columns(3)
        col1.metric("Monthly Budget", f"{budget:,.0f} ₪")
        col2.metric("Total Spent", f"{period_total:,.0f} ₪")
    
        # Dynamic coloring: Red if over budget, Green if safe
        col3.metric("Remaining", f"{remaining:,.0f} ₪", 
                delta=f"{remaining:,.0f}", 
                delta_color="normal" if remaining >= 0 else "inverse")

    st.divider()

    # Display Pie Chart
    if category_totals:
        # Generate the chart object using the helper function from charts.py
        fig = create_expense_pie_chart(category_totals)
        
        # Render the chart in Streamlit 
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info(f"No expenses recorded for {selected_period}.")
