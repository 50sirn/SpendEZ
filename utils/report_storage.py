
import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_DIR / "data"
REPORT_FILE = DATA_FOLDER / "reports.csv"

REPORT_FIELDS = [
    "report_id",
    "name",
    "description",
    "start_date",
    "end_date",
    "budget",
    "budget_currency",
    "status"
]


def add_report(report):

    DATA_FOLDER.mkdir(exist_ok=True)

    file_exists = REPORT_FILE.exists() and REPORT_FILE.stat().st_size > 0

    with open(REPORT_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=REPORT_FIELDS
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(report)


def load_reports():

    if not REPORT_FILE.exists():
        return []

    with open(REPORT_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        return list(reader)


def update_report(report_id, updates):

    reports = load_reports()

    updated = False

    for report in reports:

        if report["report_id"] == report_id:

            report.update(updates)
            updated = True
            break

    if not updated:
        return False

    DATA_FOLDER.mkdir(exist_ok=True)

    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=REPORT_FIELDS
        )

        writer.writeheader()
        writer.writerows(reports)

    return True


def delete_report(report_id):

    reports = load_reports()

    original_count = len(reports)

    reports = [
        report for report in reports
        if report["report_id"] != report_id
    ]

    if len(reports) == original_count:
        return False

    DATA_FOLDER.mkdir(exist_ok=True)

    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=REPORT_FIELDS
        )

        writer.writeheader()
        writer.writerows(reports)

    return True
