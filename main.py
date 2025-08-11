# main.py
import csv
from pathlib import Path
import datetime
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "expenses.csv"

def ensure_data_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        # create header row
        with DATA_FILE.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "amount", "description"])
        # optional small sample rows:
        sample = [
            ["2025-08-01", "Food", "120.0", "Lunch"],
            ["2025-08-02", "Travel", "50.0", "Bus"],
            ["2025-07-30", "Groceries", "560.0", "Weekly shop"],
        ]
        with DATA_FILE.open("a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(sample)

def add_expense():
    date_str = input("Date (YYYY-MM-DD) [today]: ").strip()
    if not date_str:
        date_str = datetime.date.today().isoformat()
    else:
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
    category = input("Category (e.g. Food, Travel) [Other]: ").strip() or "Other"
    amount_s = input("Amount: ").strip()
    try:
        amount = float(amount_s)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    description = input("Description (optional): ").strip()
    with DATA_FILE.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, category, amount, description])
    print("Saved ✅")

def view_expenses(n=20):
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df = df.sort_values("date", ascending=False)
    print(df.head(n).to_string(index=False))

def monthly_summary():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    if df.empty:
        print("No data.")
        return
    df["month"] = df["date"].dt.to_period("M").astype(str)
    totals = df.groupby("month")["amount"].sum().sort_index()
    print("\nMonthly totals:")
    print(totals.to_string())

def category_summary():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    if df.empty:
        print("No data.")
        return
    totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    print("\nTotals by category:")
    print(totals.to_string())

def plot_monthly_totals():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    if df.empty:
        print("No data to plot.")
        return
    df["month"] = df["date"].dt.to_period("M").astype(str)
    totals = df.groupby("month")["amount"].sum().sort_index()
    ax = totals.plot(kind="bar", legend=False)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total spent")
    ax.set_title("Monthly expenses")
    plt.tight_layout()
    plt.show()

def export_csv(filename="export.csv"):
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df.to_csv(filename, index=False)
    print(f"Exported to {filename}")

def main_menu():
    ensure_data_file()
    while True:
        print("\n1) Add expense  2) View latest  3) Monthly summary\n4) Category summary  5) Plot monthly  6) Export CSV  0) Quit")
        c = input("Choose: ").strip()
        if c == "1":
            add_expense()
        elif c == "2":
            view_expenses()
        elif c == "3":
            monthly_summary()
        elif c == "4":
            category_summary()
        elif c == "5":
            plot_monthly_totals()
        elif c == "6":
            export_csv()
        elif c == "0":
            print("Goodbye!")
            break
        else:
            print("Unknown option.")

if __name__ == "__main__":
    main_menu()
