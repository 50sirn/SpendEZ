
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
BUDGET_FILE = DATA_FOLDER / "budgets.csv"

# Create data folder if it doesn't exist
DATA_FOLDER.mkdir(exist_ok=True)

# Application title
st.title("💰 SpendEasy")
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

# Budget Management Page
elif menu == "Budget Management":
    st.header("💰 Budget Management")

    st.write("Set monthly spending limits and monitor your expenses.")

    # Budget configuration
    st.subheader("Set a Budget")

    with st.form("budget_form"):

        budget_month = st.date_input(
            "Select Budget Month",
            value=date.today()
        )

        budget_currency = st.selectbox(
            "Currency",
            currencies,
            key="budget_currency"
        )

        budget_category = st.selectbox(
            "Budget Category",
            ["Overall"] + categories
        )

        budget_amount = st.number_input(
            "Monthly Budget",
            min_value=0.01,
            step=100.0
        )

        save_budget = st.form_submit_button(
            "Save Budget"
        )

        if save_budget:

            month_string = budget_month.strftime("%Y-%m")

            new_budget = {
                "month": month_string,
                "currency": budget_currency,
                "category": budget_category,
                "budget": budget_amount
            }

            # Load existing budgets
            if BUDGET_FILE.exists():

                budgets = pd.read_csv(BUDGET_FILE)

            else:

                budgets = pd.DataFrame(
                    columns=[
                        "month",
                        "currency",
                        "category",
                        "budget"
                    ]
                )

            # Identify an existing matching budget
            matching_budget = (
                (budgets["month"] == month_string)
                & (budgets["currency"] == budget_currency)
                & (budgets["category"] == budget_category)
            )

            if matching_budget.any():

                # Update existing budget
                budgets.loc[
                    matching_budget, "budget"
                ] = budget_amount

            else:

                # Add new budget
                budgets = pd.concat(
                    [
                        budgets,
                        pd.DataFrame([new_budget])
                    ],
                    ignore_index=True
                )

            # Save budgets
            budgets.to_csv(
                BUDGET_FILE,
                index=False
            )

            st.success("Budget saved successfully!")

            st.rerun()

    st.divider()

    # Budget monitoring
    st.subheader("Budget Overview")

    if BUDGET_FILE.exists():

        budgets = pd.read_csv(BUDGET_FILE)

        selected_month = st.selectbox(
            "Select Month",
            sorted(budgets["month"].unique(), reverse=True)
        )

        selected_currency = st.selectbox(
            "Select Currency",
            currencies,
            key="overview_currency"
        )

        selected_budgets = budgets[
            (budgets["month"] == selected_month)
            & (budgets["currency"] == selected_currency)
        ]

        if not selected_budgets.empty:

            # Load expenses
            if DATA_FILE.exists():

                expenses = pd.read_csv(DATA_FILE)

                expenses["date"] = pd.to_datetime(
                    expenses["date"],
                    errors="coerce"
                )

                expenses["amount"] = pd.to_numeric(
                    expenses["amount"],
                    errors="coerce"
                )

                expenses = expenses.dropna(
                    subset=["date", "amount"]
                )

            else:

                expenses = pd.DataFrame(
                    columns=[
                        "date",
                        "amount",
                        "currency",
                        "category"
                    ]
                )

            for _, budget_row in selected_budgets.iterrows():

                category_name = budget_row["category"]
                budget_limit = float(budget_row["budget"])

                # Filter expenses by month and currency
                relevant_expenses = expenses[
                    (expenses["date"].dt.strftime("%Y-%m") == selected_month)
                    & (expenses["currency"] == selected_currency)
                ]

                # Filter by category unless this is an overall budget
                if category_name != "Overall":

                    relevant_expenses = relevant_expenses[
                        relevant_expenses["category"] == category_name
                    ]

                spent = relevant_expenses["amount"].sum()

                remaining = budget_limit - spent

                percentage = spent / budget_limit

                st.markdown(f"### {category_name}")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Budget",
                    f"{selected_currency} {budget_limit:,.2f}"
                )

                col2.metric(
                    "Spent",
                    f"{selected_currency} {spent:,.2f}"
                )

                col3.metric(
                    "Remaining",
                    f"{selected_currency} {remaining:,.2f}"
                )

                st.progress(min(percentage, 1.0))

                st.caption(
                    f"{percentage * 100:.1f}% of budget used"
                )

                if percentage >= 1:

                    st.error("Budget exceeded!")

                elif percentage >= 0.8:

                    st.warning("You're approaching your budget limit!")

                else:

                    st.success("You're within your budget.")

                st.divider()

        else:

            st.info("No budgets found for this currency and month.")

    else:

        st.info("You haven't created any budgets yet.")
