# 💰 SpendEZ

**Your Personal Expense Tracker**

SpendEZ is a Python-based personal expense tracking application built using Streamlit. It allows users to record expenses, monitor spending habits, manage monthly budgets, and visualise their financial activity through interactive dashboards.

SpendEZ supports multiple currencies and helps users keep track of their spending in one place.

##  Features

- **Expense Tracking:** Record expenses with transaction dates, amounts, currencies, categories, and descriptions.
- **Multi-Currency Support:** Track expenses in INR, USD, EUR, GBP, JPY, AUD, CAD, SGD, and AED.
- **Financial Dashboard:** View transaction statistics and analyse spending through interactive charts.
- **Category-wise Analysis:** Understand spending patterns through category-based expenditure breakdowns.
- **Monthly Spending Analysis:** Monitor spending trends across different months.
- **Budget Management:** Set monthly overall or category-specific budgets.
- **Budget Alerts:** Receive warnings when approaching or exceeding spending limits.
- **CSV Data Storage:** Store expense and budget records locally using CSV files.

##  Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Pandas | Data handling and analysis |
| CSV | Local data storage |
| Git & GitHub | Version control and project hosting |

##  Prerequisites

Before running SpendEZ, make sure you have:

- Python 3.9 or later
- pip (Python package installer)
- Git (optional, for cloning the repository)

##  Installation & Setup

Follow these steps to run SpendEZ locally.

**1. Clone the repository**

```bash
git clone https://github.com/50sirn/SpendEZ.git
```

**2. Navigate to the project directory**

```bash
cd SpendEZ
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate the virtual environment**

Windows:

```bash
venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

**6. Run the application**

```bash
python -m streamlit run app.py
```

SpendEZ will open in your default web browser.

##  Project Structure

```text
SpendEZ/
│
├── app.py
│
├── modules/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── expenses.py
│   ├── budgets.py
│   └── transactions.py
│
├── utils/
│   ├── __init__.py
│   └── storage.py
│
├── data/
│   ├── expenses.csv
│   └── budgets.csv
│
├── requirements.txt
├── .gitignore
└── README.md
```

##  Data Storage

SpendEZ uses CSV files for persistent local data storage.

- Expense records are stored in `data/expenses.csv`.
- Budget configurations are stored in `data/budgets.csv`.
- Data is loaded and updated using the storage utilities in `utils/storage.py`.
- The application automatically creates the data directory when required.

**Note:** CSV files are excluded from version control through `.gitignore` to prevent personal financial records from being accidentally uploaded to GitHub.

##  Screenshots

Screenshots of the SpendEZ application will be added here to demonstrate its interface and functionality.

Planned screenshots:

- Financial Dashboard
- Expense Entry Page
- Transaction History
- Budget Management

##  Future Improvements

Potential features planned for future versions:

- Expense editing and deletion
- Advanced transaction filtering and search
- Data visualisation enhancements
- Exportable financial reports
- Improved user interface and experience