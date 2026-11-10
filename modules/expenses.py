
import streamlit as st
from datetime import date
import uuid

from utils.storage import add_expense
from utils.report_storage import load_reports


def render_expense_page(currencies, categories):

    st.title("Add a New Expense")
    st.write("Record your spending below.")

    # Load active expense reports
    reports = load_reports()

    active_reports = [
        report for report in reports
        if report.get("status") == "Active"
    ]

    report_options = [None] + active_reports

    # Initialize form values
    defaults = {
        "expense_amount": 0.01,
        "expense_currency": currencies[0],
        "expense_category": categories[0],
        "expense_date": date.today(),
        "expense_description": "",
        "expense_report": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Handle form submission
    def save_expense():

        amount = st.session_state.expense_amount

        if amount <= 0:
            st.session_state.expense_error = "Please enter a valid amount."
            return

        selected_report = st.session_state.expense_report

        expense = {
            "transaction_id": str(uuid.uuid4()),
            "date": st.session_state.expense_date,
            "amount": amount,
            "currency": st.session_state.expense_currency,
            "category": st.session_state.expense_category,
            "description": st.session_state.expense_description,
            "report_id": selected_report["report_id"] if selected_report else ""
        }

        try:
            add_expense(expense)

            # Reset all form fields
            st.session_state.expense_amount = 0.01
            st.session_state.expense_currency = currencies[0]
            st.session_state.expense_category = categories[0]
            st.session_state.expense_date = date.today()
            st.session_state.expense_description = ""
            st.session_state.expense_report = None

            st.session_state.expense_saved = True
            st.session_state.expense_error = None

        except Exception as error:
            st.session_state.expense_error = f"Could not save expense: {error}"

    # Expense form
    with st.form("expense_form"):

        st.number_input(
            "Amount",
            min_value=0.01,
            step=1.0,
            key="expense_amount"
        )

        st.selectbox(
            "Currency",
            currencies,
            key="expense_currency"
        )

        st.selectbox(
            "Category",
            categories,
            key="expense_category"
        )

        st.date_input(
            "Date",
            key="expense_date"
        )

        st.text_input(
            "Description",
            placeholder="What did you spend on?",
            key="expense_description"
        )

        st.selectbox(
            "Expense Report (Optional)",
            report_options,
            format_func=lambda report: (
                "No report" if report is None else report["name"]
            ),
            key="expense_report"
        )

        st.form_submit_button(
            "Add Expense",
            on_click=save_expense
        )

    # Display feedback
    if st.session_state.get("expense_error"):
        st.error(st.session_state.expense_error)

    if st.session_state.get("expense_saved", False):
        st.toast("Expense added successfully!", icon="✅")
        st.session_state.expense_saved = False
