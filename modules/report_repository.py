
import streamlit as st
from datetime import date

from utils.report_storage import load_reports, update_report, delete_report
from utils.storage import load_expenses, handle_report_expenses


def clear_report_search():
    st.session_state.report_search = ""


def handle_report_deletion(report_id, delete_transactions):

    try:

        deleted = delete_report(report_id)

        if not deleted:
            st.session_state.report_delete_result = {
                "success": False
            }
            return

        affected_count = handle_report_expenses(
            report_id,
            delete_transactions
        )

        st.session_state.report_delete_result = {
            "success": True,
            "count": affected_count,
            "transactions_deleted": delete_transactions
        }

        # Return to the repository listing
        st.session_state.selected_report_id = None
        st.session_state.edit_mode = False

    except Exception as error:

        st.session_state.report_delete_result = {
            "success": False,
            "error": str(error)
        }


def initialize_edit_form(report, currencies):

    st.session_state.edit_report_name = report.get("name", "")
    st.session_state.edit_report_description = report.get("description", "")

    st.session_state.edit_report_start_date = (
        date.fromisoformat(report["start_date"])
        if report.get("start_date") else date.today()
    )

    st.session_state.edit_report_has_end_date = bool(
        report.get("end_date")
    )

    st.session_state.edit_report_end_date = (
        date.fromisoformat(report["end_date"])
        if report.get("end_date") else date.today()
    )

    st.session_state.edit_report_budget = float(
        report.get("budget") or 0
    )

    current_currency = report.get("budget_currency", "")

    st.session_state.edit_report_budget_currency = (
        current_currency if current_currency in currencies
        else currencies[0]
    )

    st.session_state.edit_report_status = report.get("status", "Active")
    st.session_state.edit_mode = True
    st.session_state.edit_error = None


def save_report_changes(report_id):

    name = st.session_state.edit_report_name.strip()
    start_date = st.session_state.edit_report_start_date
    has_end_date = st.session_state.edit_report_has_end_date
    end_date = st.session_state.edit_report_end_date
    budget = st.session_state.edit_report_budget

    if not name:
        st.session_state.edit_error = "Please enter a report name."
        return

    if has_end_date and end_date < start_date:
        st.session_state.edit_error = (
            "End date cannot be before the start date."
        )
        return

    updates = {
        "name": name,
        "description": st.session_state.edit_report_description.strip(),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat() if has_end_date else "",
        "budget": budget if budget > 0 else "",
        "budget_currency": (
            st.session_state.edit_report_budget_currency
            if budget > 0 else ""
        ),
        "status": st.session_state.edit_report_status
    }

    try:
        success = update_report(report_id, updates)

        if success:
            st.session_state.edit_mode = False
            st.session_state.edit_error = None
            st.session_state.edit_saved = True
        else:
            st.session_state.edit_error = "Could not find this report."

    except Exception as error:
        st.session_state.edit_error = (
            f"Could not update report: {error}"
        )


def render_report_repository(currencies):

    selected_id = st.session_state.get("selected_report_id")
    reports = load_reports()
    if "report_delete_result" in st.session_state:

        result = st.session_state.report_delete_result

        if result["success"]:

            if result["transactions_deleted"]:
                st.toast(
                    f"Report and {result['count']} linked transactions deleted!",
                    icon="✅"
                )
            else:
                st.toast(
                    f"Report deleted! {result['count']} transactions preserved.",
                    icon="✅"
                )

        else:
            st.error(
                result.get("error", "Could not delete the report.")
            )

        del st.session_state.report_delete_result

    # Individual report view
    if selected_id:

        report = next(
            (r for r in reports if r["report_id"] == selected_id),
            None
        )

        if report is None:
            st.session_state.selected_report_id = None
            st.rerun()
            return

        if st.button("← Back to Reports"):
            st.session_state.selected_report_id = None
            st.rerun()

        st.title(report["name"])

        if report.get("description"):
            st.write(report["description"])

        st.caption(
            f"Status: {report.get('status', 'Active')} | "
            f"Start Date: {report.get('start_date', 'N/A')}"
        )

        if report.get("end_date"):
            st.caption(f"End Date: {report['end_date']}")

        # Edit report
        if not st.session_state.get("edit_mode", False):

            if st.button(
                "✏️ Edit Report",
                key="edit_report_button"
            ):
                initialize_edit_form(report, currencies)
                st.rerun()

        else:

            st.divider()
            st.subheader("Edit Expense Report")

            with st.form("edit_report_form"):

                st.text_input(
                    "Report Name",
                    key="edit_report_name"
                )

                st.text_area(
                    "Description",
                    key="edit_report_description"
                )

                st.divider()
                st.subheader("Duration")

                st.date_input(
                    "Start Date",
                    key="edit_report_start_date"
                )

                st.checkbox(
                    "Include an end date",
                    key="edit_report_has_end_date"
                )

                st.date_input(
                    "End Date",
                    key="edit_report_end_date"
                )

                st.divider()
                st.subheader("Budget")

                st.number_input(
                    "Budget Amount (Enter 0 if no budget)",
                    min_value=0.0,
                    step=100.0,
                    key="edit_report_budget"
                )

                st.selectbox(
                    "Budget Currency",
                    currencies,
                    key="edit_report_budget_currency"
                )

                st.selectbox(
                    "Report Status",
                    ["Active", "Completed"],
                    key="edit_report_status"
                )

                save_button, cancel_button = st.columns(2)

                with save_button:
                    save_clicked = st.form_submit_button(
                        "Save Changes"
                    )

                with cancel_button:
                    cancel_clicked = st.form_submit_button(
                        "Cancel"
                    )

            if save_clicked:
                save_report_changes(selected_id)
                st.rerun()

            if cancel_clicked:
                st.session_state.edit_mode = False
                st.rerun()

            if st.session_state.get("edit_error"):
                st.error(st.session_state.edit_error)

        if st.session_state.get("edit_saved", False):
            st.toast("Report updated successfully!", icon="✅")
            st.session_state.edit_saved = False

        st.divider()

        # Report expenses
        expenses = load_expenses()

        if "report_id" not in expenses.columns:
            expenses["report_id"] = ""

        report_expenses = expenses[
            expenses["report_id"].fillna("").astype(str)
            == str(selected_id)
        ].copy()

        st.divider()
        st.subheader("🗑️ Delete Expense Report")

        st.warning(
            "Deleting this report is permanent. "
            "Choose what should happen to its linked transactions."
        )

        delete_linked = st.checkbox(
            f"Also permanently delete all {len(report_expenses)} "
            "transactions linked to this report",
            key=f"delete_linked_{selected_id}"
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this report.",
            key=f"confirm_report_delete_{selected_id}"
        )

        st.button(
            "Delete Report",
            type="primary",
            disabled=not confirm_delete,
            key=f"delete_report_{selected_id}",
            on_click=handle_report_deletion,
            args=(selected_id, delete_linked)
        )


        st.subheader("Report Summary")

        transaction_count = len(report_expenses)
        st.metric("Total Transactions", transaction_count)

        if transaction_count > 0:

            currency_totals = (
                report_expenses.groupby("currency")["amount"].sum()
            )

            st.write("### Expenditure by Currency")

            for currency, total in currency_totals.items():
                st.metric(f"Total ({currency})", f"{total:,.2f}")

            st.write("### Category Breakdown")

            category_totals = (
                report_expenses.groupby("category")["amount"].sum()
            )

            st.bar_chart(category_totals)

            st.write("### Transactions")

            st.dataframe(
                report_expenses[
                    ["date", "description", "category", "amount", "currency"]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No expenses have been linked to this report yet.")

        # Budget overview
        if report.get("budget"):

            budget = float(report["budget"])
            budget_currency = report.get("budget_currency", "")

            matching_currency_total = (
                report_expenses[
                    report_expenses["currency"] == budget_currency
                ]["amount"].sum()
            )

            st.divider()
            st.subheader("Budget Overview")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Budget",
                    f"{budget:,.2f} {budget_currency}"
                )

            with col2:
                st.metric(
                    "Remaining",
                    f"{budget - matching_currency_total:,.2f} "
                    f"{budget_currency}"
                )

        return

    # Repository listing
    st.title("Expense Report Repository")
    st.write("View and manage all your expense reports.")

    if not reports:
        st.info("You haven't created any expense reports yet.")
        return

    # Search
    st.subheader("Find a Report")

    search_col, clear_col = st.columns([5, 1])

    with search_col:
        st.text_input(
            "Search reports",
            placeholder="Search by report name or description...",
            key="report_search"
        )

    with clear_col:
        st.write("")
        st.button(
            "Clear",
            on_click=clear_report_search,
            disabled=not st.session_state.get("report_search", "")
        )

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Active", "Completed"],
        key="report_status_filter"
    )

    search_query = st.session_state.get(
        "report_search", ""
    ).strip().lower()

    filtered_reports = []

    for report in reports:

        name = report.get("name", "").lower()
        description = report.get("description", "").lower()
        status = report.get("status", "Active")

        matches_search = (
            search_query in name or search_query in description
        )

        matches_status = (
            status_filter == "All" or status == status_filter
        )

        if matches_search and matches_status:
            filtered_reports.append(report)

    st.divider()

    st.subheader(f"Your Reports ({len(filtered_reports)})")

    if not filtered_reports:
        st.warning("No reports match your search or selected filter.")
        return

    columns = st.columns(2)

    for index, report in enumerate(filtered_reports):

        with columns[index % 2]:

            with st.container(border=True):

                st.subheader(report["name"])

                if report.get("description"):
                    st.write(report["description"])

                status = report.get("status", "Active")

                if status == "Active":
                    st.success("Active")
                else:
                    st.info(status)

                st.caption(
                    f"Start Date: {report.get('start_date', 'N/A')}"
                )

                if report.get("end_date"):
                    st.caption(f"End Date: {report['end_date']}")

                if report.get("budget"):
                    st.write(
                        f"Budget: {report['budget']} "
                        f"{report.get('budget_currency', '')}"
                    )

                if st.button(
                    "View Report",
                    key=f"view_report_{report['report_id']}"
                ):
                    st.session_state.selected_report_id = report["report_id"]
                    st.rerun()
