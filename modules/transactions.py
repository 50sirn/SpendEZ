
import streamlit as st
import pandas as pd

from utils.storage import load_expenses, delete_expense


def render_transactions():

    st.header("📋 Your Transactions")

    expenses = load_expenses()

    if not expenses.empty:

        st.dataframe(
            expenses,
            width="stretch"
        )

        st.divider()

        st.subheader("🗑️ Delete a Transaction")

        transaction_options = {}

        for _, expense in expenses.iterrows():

            transaction_id = str(expense["transaction_id"])

            label = (
                f"{expense['date']} | "
                f"{expense['category']} | "
                f"{expense['amount']} {expense['currency']} | "
                f"{expense['description']}"
            )

            transaction_options[label] = transaction_id

        selected_label = st.selectbox(
            "Select the transaction you want to delete",
            options=list(transaction_options.keys())
        )

        selected_id = transaction_options[selected_label]

        selected_expense = expenses[
            expenses["transaction_id"].astype(str) == selected_id
        ].iloc[0]

        st.write("**Transaction Details**")

        st.write(f"Date: {selected_expense['date']}")
        st.write(f"Category: {selected_expense['category']}")
        st.write(
            f"Amount: {selected_expense['amount']} "
            f"{selected_expense['currency']}"
        )
        st.write(f"Description: {selected_expense['description']}")

        report_id = selected_expense["report_id"]

        if pd.notna(report_id) and str(report_id).strip():
            st.caption("This transaction is linked to an expense report.")

        confirm_delete = st.checkbox(
            "I understand that this transaction will be permanently deleted.",
            key=f"confirm_delete_{selected_id}"
        )

        def handle_delete(transaction_id):

            deleted = delete_expense(transaction_id)

            st.session_state["transaction_delete_result"] = deleted

        st.button(
            "Delete Transaction",
            type="primary",
            disabled=not confirm_delete,
            on_click=handle_delete,
            args=(selected_id,)
        )

    else:

        st.info("No expenses recorded yet.")

    if "transaction_delete_result" in st.session_state:

        if st.session_state["transaction_delete_result"]:
            st.toast("Transaction deleted successfully!", icon="✅")
        else:
            st.error("Could not find the selected transaction.")

        del st.session_state["transaction_delete_result"]
