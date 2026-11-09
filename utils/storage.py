
import pandas as pd
from pathlib import Path

# Define storage locations
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_DIR / "data"

EXPENSE_FILE = DATA_FOLDER / "expenses.csv"
BUDGET_FILE = DATA_FOLDER / "budgets.csv"

# Ensure data directory exists
DATA_FOLDER.mkdir(exist_ok=True)


# Load expense records
def load_expenses():

    if EXPENSE_FILE.exists():
        return pd.read_csv(EXPENSE_FILE)

    return pd.DataFrame(columns=[
        "transaction_id",
        "date",
        "amount",
        "currency",
        "category",
        "description"
    ])


# Save a new expense
def add_expense(expense):

    expense_df = pd.DataFrame([expense])

    expense_df.to_csv(
        EXPENSE_FILE,
        mode="a",
        header=not EXPENSE_FILE.exists(),
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
