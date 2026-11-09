
import streamlit as st
import pandas as pd
from datetime import date

from utils.storage import load_budgets, save_budgets, load_expenses


def render_budgets(currencies, categories):

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

        save_budget = st.form_submit_button("Save Budget")

        if save_budget:

            month_string = budget_month.strftime("%Y-%m")

            new_budget = {
                "month": month_string,
                "currency": budget_currency,
                "category": budget_category,
                "budget": budget_amount
            }

            budgets = load_budgets()

            matching_budget = (
                (budgets["month"] == month_string)
                & (budgets["currency"] == budget_currency)
                & (budgets["category"] == budget_category)
            )

            if matching_budget.any():

                budgets.loc[
                    matching_budget, "budget"
                ] = budget_amount

            else:

                budgets = pd.concat(
                    [
                        budgets,
                        pd.DataFrame([new_budget])
                    ],
                    ignore_index=True
                )

            save_budgets(budgets)

            st.success("Budget saved successfully!")

            st.rerun()

    st.divider()

    # Budget monitoring
    st.subheader("Budget Overview")

    budgets = load_budgets()

    if not budgets.empty:

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

            expenses = load_expenses()

            if not expenses.empty:

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

                # Calculate spending for this budget
                if expenses.empty:

                    spent = 0

                else:

                    # Filter expenses by month and currency
                    relevant_expenses = expenses[
                        (expenses["date"].dt.strftime("%Y-%m") == selected_month)
                        & (expenses["currency"] == selected_currency)
                    ]

                    # Filter by category
                    if category_name != "Overall":

                        relevant_expenses = relevant_expenses[
                            relevant_expenses["category"] == category_name
                        ]

                    spent = relevant_expenses["amount"].sum()

                if budget_limit <= 0:
                    remaining = 0 if spent <= 0 else -spent
                    percentage = 1.0 if spent > 0 else 0.0
                else:
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
