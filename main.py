import ttkbootstrap as tb
from ttkbootstrap.constants import *
from expense_manager import ExpenseManager
from gui.add_transaction_tab import create_add_tab
from gui.view_transactions_tab import create_view_tab
from gui.daily_summary_tab import create_summary_tab

manager = ExpenseManager()

root = tb.Window(themename="darkly")
root.title("Expense Tracker")
root.geometry("800x600")

# Optional icon
# root.iconbitmap('assets/icon.ico')

tab_control = tb.Notebook(root)
tab_control.pack(expand=1, fill="both")

create_add_tab(tab_control, manager)
create_view_tab(tab_control, manager)
create_summary_tab(tab_control, manager)

print("Tabs created, starting mainloop...")

try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nApplication exited by user.")
