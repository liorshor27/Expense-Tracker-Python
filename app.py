import streamlit as st
from classes import ExpenseManager, Expense
from datetime import datetime 

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

# --- Main Display Area ---

# Create two tabs: one for the raw list, one for analytics
tab1, tab2 = st.tabs(["📋 List", "📊 Report"])

with tab1:
    # --- Tab 1: Expense List & Management ---
    st.subheader("Your Expenses")
    
    #Check if there are expenses to display
    if manager.expenses:
        #Convert Expense objects to a list of dictionaries.
        #Streamlit requires this format to render tables.
        data = []
        i=1
        for exp in manager.expenses:
            data.append({"Index": i, "Date": exp.date, "Category": exp.category, "Name": exp.name, "Amount": f"{exp.amount} NIS"})
            i+=1
        
        #Render the static table
        st.table(data)
        
        # --- Deletion Section ---
        st.divider()
        st.write("### Delete Expense")

        #Numeric input for selecting the item index
        del_num = st.number_input("Enter Index to delete", min_value=1, step=1)
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
    st.subheader("Expenses by Category")
    
    #Aggregate expenses by category using a dictionary
    totals = {}
    for exp in manager.expenses:
        cat = exp.category
        try:
            amt = float(exp.amount)
            #If category exists add to it, otherwise initialize with 0
            totals[cat] = totals.get(cat, 0) + amt
        except:
            pass #Skip invalid amounts
    
    #If we have data, display chart and total sum
    if totals:
        st.bar_chart(totals)
        st.write(f"**Total Spent: {sum(totals.values())} NIS**")