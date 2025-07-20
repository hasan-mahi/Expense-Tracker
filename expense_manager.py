import csv
from datetime import datetime
import os
from collections import defaultdict

class ExpenseManager:
    def __init__(self, filename='data/expenses.csv'):
        self.filename = filename
        # Ensure the file and folder exist
        if not os.path.exists(self.filename):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, mode='w', newline='') as file:
                file.write('/ndate,category,type,amount,description')

    def add_transaction(self, category, txn_type, amount, description="", date=None):
        # Allow custom date or fallback to today
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, txn_type, amount, description])
        print("Transaction added successfully!")

    def view_transactions(self):
        if not os.path.exists(self.filename):
            print("No transactions found.")
            return

        with open(self.filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            try:
                header = next(reader)
            except StopIteration:
                print("No transactions found.")
                return

            rows_found = False
            for row in reader:
                rows_found = True
                print(row)

            if not rows_found:
                print("No transactions found.")

    def show_daily_summary(self):
        if not os.path.exists(self.filename):
            print("No transactions found.")
            return

        daily_data = defaultdict(lambda: {"Income": 0.0, "Expense": 0.0})

        with open(self.filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header

            for row in reader:
                if len(row) < 5:
                    continue  # skip bad rows
                date, category, txn_type, amount, _ = row
                try:
                    amount = float(amount)
                except ValueError:
                    continue

                if txn_type.lower() == 'income':
                    daily_data[date]["Income"] += amount
                elif txn_type.lower() == 'expense':
                    daily_data[date]["Expense"] += amount

        print("\n📊 Daily Summary:")
        print(f"{'Date':<12} {'Income':>10} {'Expense':>10} {'Net':>10}")
        print("-" * 44)
        for date in sorted(daily_data):
            income = daily_data[date]["Income"]
            expense = daily_data[date]["Expense"]
            net = income - expense
            print(f"{date:<12} {income:>10.2f} {expense:>10.2f} {net:>10.2f}")
