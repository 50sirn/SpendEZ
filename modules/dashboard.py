
import streamlit as st
import pandas as pd

from utils.storage import load_expenses


def render_dashboard():

    st.header("📊 Financial Dashboard")

    expenses = load_expenses()

    if not expenses.empty:

        # Prepare the data
        expenses["amount"] = pd.to_numeric(
            expenses["amount"],
            errors="coerce"
        )

        expenses["date"] = pd.to_datetime(
            expenses["date"],
            errors="coerce"
        )

        expenses = expenses.dropna(
            subset=["amount", "date"]
        )

        if expenses.empty:
            st.info("No valid expenses recorded yet.")
            return

        # Spending overview
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
