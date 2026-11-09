
import streamlit as st

from modules.expenses import render_expense_page
from modules.dashboard import render_dashboard
from modules.transactions import render_transactions
from modules.budgets import render_budgets

# Application configuration
st.set_page_config(
    page_title="SpendEZ",
    page_icon="💰",
    layout="wide"
)

# Application title
st.title("💰 SpendEZ")
st.subheader("Your Personal Expense Tracker")

# Navigation
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Add Expense", "View Expenses","Budget Management"]
)

# Available options
currencies = [
    "INR", "USD", "EUR", "GBP",
    "JPY", "AUD", "CAD", "SGD", "AED"
]

categories = [
    "Food",
    "Travel",
    "Shopping",
    "Entertainment",
    "Bills",
    "Education",
    "Healthcare",
    "Other"
]

# Add Expense Page
if menu == "Add Expense":
    render_expense_page(currencies, categories)

# Dashboard Page

elif menu == "Dashboard":
    render_dashboard()

# View Expenses Page
elif menu == "View Expenses":
    render_transactions()

# Budget Management Page
elif menu == "Budget Management":
    render_budgets(currencies, categories)
