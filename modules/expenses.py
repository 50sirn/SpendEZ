
import streamlit as st
from datetime import date
import uuid

from utils.storage import add_expense


def render_expense_page(currencies, categories):

    st.title("Add a New Expense")
    st.write("Record your spending below.")

    with st.form("expense_form"):

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            step=1.0
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

        submitted = st.form_submit_button("Add Expense")

        if submitted:

            if amount <= 0:
                st.error("Please enter a valid amount.")

            else:

                expense = {
                    "transaction_id": str(uuid.uuid4()),
                    "date": expense_date,
                    "amount": amount,
                    "currency": currency,
                    "category": category,
                    "description": description
                }

                add_expense(expense)

                st.success("Expense added successfully!")
