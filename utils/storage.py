
import pandas as pd
from pathlib import Path

# Define storage locations
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_DIR / "data"

EXPENSE_FILE = DATA_FOLDER / "expenses.csv"
BUDGET_FILE = DATA_FOLDER / "budgets.csv"

# Ensure data directory exists
DATA_FOLDER.mkdir(exist_ok=True)

# Expense database structure
EXPENSE_COLUMNS = [
    "transaction_id",
    "date",
    "amount",
    "currency",
    "category",
    "description",
    "report_id"
]


# Load expense records
def load_expenses():

    if EXPENSE_FILE.exists():
        expenses = pd.read_csv(EXPENSE_FILE)

        if "report_id" not in expenses.columns:
            expenses["report_id"] = ""

        return expenses

    return pd.DataFrame(columns=EXPENSE_COLUMNS)


# Save a new expense
def add_expense(expense):

    expenses = load_expenses()

    new_expense = {
        column: expense.get(column, "")
        for column in EXPENSE_COLUMNS
    }

    new_row = pd.DataFrame([new_expense])
    expenses = pd.concat([expenses, new_row], ignore_index=True)

    expenses.to_csv(
        EXPENSE_FILE,
        index=False
    )


# Load budget records
def load_budgets():

    if BUDGET_FILE.exists():
        return pd.read_csv(BUDGET_FILE)

    return pd.DataFrame(columns=[
        "month",
        "currency",
        "category",
        "budget"
    ])


# Save all budget records
def save_budgets(budgets):

    budgets.to_csv(
        BUDGET_FILE,
        index=False
    )
