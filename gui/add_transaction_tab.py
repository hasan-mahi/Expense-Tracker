import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from ttkbootstrap.widgets import DateEntry

def create_add_tab(tab_control, manager):
    tab = tb.Frame(tab_control)
    tab_control.add(tab, text='➕ Add Transaction')

    # --- Date Picker ---
    tb.Label(tab, text="Date:").grid(column=0, row=0, padx=10, pady=10)
    entry_date = DateEntry(tab, width=30, bootstyle="primary")  # calendar picker
    entry_date.grid(column=1, row=0)

    # --- Category ---
    tb.Label(tab, text="Category:").grid(column=0, row=1, padx=10, pady=10)
    entry_category = tb.Entry(tab, width=30)
    entry_category.insert(0, "Food")  # default value
    entry_category.grid(column=1, row=1)

    # --- Type Dropdown ---
    tb.Label(tab, text="Type:").grid(column=0, row=2, padx=10, pady=10)
    combo_type = tb.Combobox(tab, values=["Income", "Expense"], width=28, state="readonly")
    combo_type.set("Expense")  # default value
    combo_type.grid(column=1, row=2)

    # --- Amount ---
    tb.Label(tab, text="Amount:").grid(column=0, row=3, padx=10, pady=10)
    entry_amount = tb.Entry(tab, width=30)
    entry_amount.grid(column=1, row=3)

    # --- Description ---
    tb.Label(tab, text="Description:").grid(column=0, row=4, padx=10, pady=10)
    entry_description = tb.Entry(tab, width=30)
    entry_description.grid(column=1, row=4)

    # --- Submit Function ---
    def add_transaction_gui():
        date = entry_date.entry.get()
        category = entry_category.get()
        txn_type = combo_type.get()
        try:
            amount = float(entry_amount.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return
        description = entry_description.get()
        if txn_type not in ['Income', 'Expense']:
            messagebox.showerror("Error", "Type must be 'Income' or 'Expense'.")
            return

        manager.add_transaction(category, txn_type, amount, description, date=date)
        messagebox.showinfo("Success", "Transaction added.")

        entry_category.delete(0, 'end')
        entry_category.insert(0, "Food")
        combo_type.set("Expense")
        entry_amount.delete(0, 'end')
        entry_description.delete(0, 'end')

    tb.Button(tab, text="Add Transaction", command=add_transaction_gui, bootstyle="success").grid(column=1, row=5, pady=20)
