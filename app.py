
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date
import uuid

# Application configuration
st.set_page_config(
    page_title="SpendEasy",
    page_icon="💰",
    layout="wide"
)

# File configuration
DATA_FOLDER = Path("data")
DATA_FILE = DATA_FOLDER / "expenses.csv"

# Create data folder if it doesn't exist
DATA_FOLDER.mkdir(exist_ok=True)

# Application title
st.title("💰 SpendEasy")
st.subheader("Your Personal Expense Tracker")

# Navigation
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Add Expense", "View Expenses"]
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

    st.header("➕ Add a New Expense")

    with st.form("expense_form"):

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=0.01
        )

        currency = st.selectbox(
            "Currency",
            currencies
        )

        category = st.selectbox(
            "Category",
            categories
        )

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        description = st.text_input(
            "Description",
            placeholder="What did you spend on?"
        )

        submitted = st.form_submit_button(
            "Save Expense"
        )

        if submitted:

            new_expense = {
                "transaction_id": str(uuid.uuid4()),
                "date": expense_date.isoformat(),
                "amount": amount,
                "currency": currency,
                "category": category,
                "description": description
            }

            expense_df = pd.DataFrame([new_expense])

            expense_df.to_csv(
                DATA_FILE,
                mode="a",
                header=not DATA_FILE.exists(),
                index=False
            )

            st.success("Expense saved successfully!")

# Dashboard Page
elif menu == "Dashboard":

    st.header("📊 Dashboard")
    st.write("Your financial overview will appear here.")

# View Expenses Page
elif menu == "View Expenses":

    st.header("📋 Your Transactions")

    if DATA_FILE.exists():

        expenses = pd.read_csv(DATA_FILE)

        st.dataframe(
            expenses,
            use_container_width=True
        )

    else:

        st.info("No expenses recorded yet.")
