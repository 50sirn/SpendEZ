
import streamlit as st
from datetime import date
import uuid

from utils.report_storage import add_report


def render_create_report(currencies):

    st.title("Create Expense Report")
    st.write("Create a separate report for a trip, event, activity or any other purpose.")

    # Initialize form values
    defaults = {
        "report_name": "",
        "report_description": "",
        "report_start_date": date.today(),
        "report_has_end_date": False,
        "report_end_date": date.today(),
        "report_budget": 0.0,
        "report_budget_currency": "INR"
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Save report callback
    def save_report():

        name = st.session_state.report_name.strip()
        start_date = st.session_state.report_start_date
        has_end_date = st.session_state.report_has_end_date
        end_date = st.session_state.report_end_date
        budget = st.session_state.report_budget

        if not name:
            st.session_state.report_error = "Please enter a report name."
            return

        if has_end_date and end_date < start_date:
            st.session_state.report_error = "End date cannot be before the start date."
            return

        report = {
            "report_id": str(uuid.uuid4()),
            "name": name,
            "description": st.session_state.report_description.strip(),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat() if has_end_date else "",
            "budget": budget if budget > 0 else "",
            "budget_currency": st.session_state.report_budget_currency if budget > 0 else "",
            "status": "Active"
        }

        try:
            add_report(report)

            # Reset form fields
            for key, value in defaults.items():
                st.session_state[key] = value

            st.session_state.report_error = None
            st.session_state.report_saved = True

        except Exception as error:
            st.session_state.report_error = f"Could not create report: {error}"

    # Report creation form
    with st.form("create_report_form"):

        st.subheader("Report Details")

        st.text_input(
            "Report Name",
            placeholder="e.g. Shillong Family Trip",
            key="report_name"
        )

        st.text_area(
            "Description (Optional)",
            placeholder="What is this report for?",
            key="report_description"
        )

        st.divider()

        st.subheader("Duration")

        st.date_input(
            "Start Date",
            key="report_start_date"
        )

        
        st.checkbox(
            "Include an end date",
            key="report_has_end_date"
        )

        st.date_input(
            "End Date",
            key="report_end_date"
        )


        st.divider()

        st.subheader("Budget (Optional)")

        st.number_input(
            "Budget Amount (Enter 0 if no budget)",
            min_value=0.0,
            step=100.0,
            key="report_budget"
        )

        st.selectbox(
            "Budget Currency",
            currencies,
            key="report_budget_currency"
        )

        st.form_submit_button(
            "Create Report",
            on_click=save_report
        )

    # Display feedback
    if st.session_state.get("report_error"):
        st.error(st.session_state.report_error)

    if st.session_state.get("report_saved", False):
        st.toast("Expense report created successfully!", icon="✅")
        st.session_state.report_saved = False
