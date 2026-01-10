#💰Expense Tracker App

A smart expense tracking application built with **Python**. 
This project demonstrates modular architecture, Object-Oriented Programming (OOP), and features both a **Command Line Interface (CLI)** and a modern **Web Dashboard** using Streamlit.

##🚀Features

* **Dual Interface:** Run it as a simple CLI tool or a full Web App.
* **Data Persistence:** Automatically saves and loads data using CSV.
* **Smart Analytics:** View expenses by category with automatic aggregation.
* **Input Validation:** Robust error handling for dates and amounts.
* **Interactive UI:** (Web Mode) Filter, view tables, and delete records visually.

##🛠️ Tech Stack

* **Language:** Python 3.10+
* **GUI Framework:** Streamlit
* **Data Storage:** CSV (File I/O)
* **Libraries:** `datetime`, `csv`, `os`

## 📂 Project Structure

* `app.py` - Main entry point for the Web Application (Streamlit).
* `main.py` - Main entry point for the Command Line Interface (CLI).
* `classes.py` - Logic layer containing `Expense` and `ExpenseManager` classes.
* `charts.py` - Handles data visualization and graph generation (Plotly).
* `styles.py` - Manages the CSS and visual styling of the application.
* `validations.py` - Helper functions for robust input validation.
* `utils.py` - Contains helper functions for date parsing, data filtering, and trend analysis logic.

##💻 How to Run

### 1. Web Dashboard (Recommended)
```bash
pip install streamlit
streamlit run app.py
