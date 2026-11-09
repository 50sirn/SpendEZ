
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

    st.header("📊 Financial Dashboard")

    if DATA_FILE.exists():

        expenses = pd.read_csv(DATA_FILE)

        if not expenses.empty:

            # Prepare the data
            expenses["amount"] = pd.to_numeric(
                expenses["amount"], errors="coerce"
            )

            expenses["date"] = pd.to_datetime(
                expenses["date"], errors="coerce"
            )

            expenses = expenses.dropna(
                subset=["amount", "date"]
            )

            # Overview
            st.subheader("Your Spending Overview")

            total_transactions = len(expenses)
            total_currencies = expenses["currency"].nunique()

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Transactions",
                total_transactions
            )

            col2.metric(
                "Currencies Used",
                total_currencies
            )

            # Currency-wise expenditure
            st.subheader("Expenditure by Currency")

            currency_totals = (
                expenses.groupby("currency")["amount"].sum()
            )

            cols = st.columns(3)

            for index, (currency, total) in enumerate(
                currency_totals.items()
            ):

                with cols[index % 3]:

                    st.metric(
                        label=f"Total in {currency}",
                        value=f"{total:,.2f}"
                    )

            # Currency filter
            st.divider()

            selected_currency = st.selectbox(
                "Analyse spending in:",
                sorted(expenses["currency"].unique())
            )

            filtered_expenses = expenses[
                expenses["currency"] == selected_currency
            ]

            # Category analysis
            st.subheader(
                f"Spending by Category ({selected_currency})"
            )

            category_totals = (
                filtered_expenses.groupby("category")["amount"]
                .sum()
                .sort_values(ascending=False)
            )

            st.bar_chart(category_totals)

            # Monthly analysis
            st.subheader(
                f"Monthly Spending ({selected_currency})"
            )

            filtered_expenses = filtered_expenses.copy()

            filtered_expenses["month"] = (
                filtered_expenses["date"].dt.to_period("M")
            )

            monthly_totals = (
                filtered_expenses.groupby("month")["amount"]
                .sum()
            )

            monthly_totals.index = (
                monthly_totals.index.astype(str)
            )

            st.line_chart(monthly_totals)

        else:

            st.info("No expenses recorded yet.")

    else:

        st.info("No expenses recorded yet.")


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
