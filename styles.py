import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* 1. Main App Background (Dark Sea Green) */
        .stApp {
            background-color: #8FBC8F;
        }
        
        /* 2. Headers: Dark green, clean font, centered */
        h1, h1 span, h2, h3, h2 span, h3 span {
            color: #004d00 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            text-align: center;
        }
        
        /* 3. Buttons: Dark green background, white text */
        .stButton>button {
            background-color: #2E8B57 !important;
            color: white !important;
            border-radius: 8px;
            font-size: 16px;
            width: 100%;
            border: none;
        }
        
        /* 4. Sidebar: Light green background */
        [data-testid="stSidebar"] {
            background-color: #90EE90;
            border-right: 1px solid #ddd;
        }
        
        /* 5. Input Fields: Beige background with dark border */
        input, .stDateInput input, .stSelectbox div[data-baseweb="select"] > div {
            background-color: #F5F5DC !important;
            color: black !important;
            border: 1px solid #004d00; 
        }
        
        /* Fix for Selectbox Arrow Icon */
        div[data-baseweb="select"] svg {
            fill: black !important;
        }
        
        /* Fix for Number Input +/- Buttons */
        [data-testid="stNumberInput"] button {
             background-color: #F5F5DC !important;
             color: black !important;
        }

        /* 6. Table Styling */
        
        /* General table structure */
        [data-testid="stTable"] table {
            border-collapse: collapse !important; 
            width: 100%;
        }

        /* Table Headers (th) and Cells (td) */
        [data-testid="stTable"] th, [data-testid="stTable"] td {
            /* RGBA for transparency: 0.7 = 70% opacity */
            background-color: rgba(245, 245, 220, 0.7) !important; 
            
            color: black !important;              
            border: 1px solid black !important;   
            padding: 8px !important;              
        }
        </style>
    """, unsafe_allow_html=True)