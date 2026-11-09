
import streamlit as st

from utils.storage import load_expenses


def render_transactions():

    st.header("📋 Your Transactions")

    expenses = load_expenses()

    if not expenses.empty:

        st.dataframe(
            expenses,
            width="stretch"
        )

    else:

        st.info("No expenses recorded yet.")
