import ttkbootstrap as tb
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def create_summary_tab(tab_control, manager):
    tab = tb.Frame(tab_control)
    tab_control.add(tab, text='📊 Daily Summary')

    tree = tb.Treeview(tab, columns=("Date", "Income", "Expense", "Net"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=140)
    tree.pack(expand=True, fill='both')

    canvas_container = tb.Frame(tab)  # container to hold the chart canvas
    canvas_container.pack(fill='both', expand=False, pady=10)

    canvas = None  # store current canvas reference

    def load_summary():
        tree.delete(*tree.get_children())
        daily_data = defaultdict(lambda: {"Income": 0.0, "Expense": 0.0})

        with open(manager.filename, 'r') as file:
            next(file)  # skip header
            for line in file:
                date, category, txn_type, amount, _ = line.strip().split(',')
                amount = float(amount)
                if txn_type.lower() == 'income':
                    daily_data[date]["Income"] += amount
                elif txn_type.lower() == 'expense':
                    daily_data[date]["Expense"] += amount

        for date in sorted(daily_data):
            income = daily_data[date]["Income"]
            expense = daily_data[date]["Expense"]
            net = income - expense
            tree.insert('', 'end', values=(date, f"{income:.2f}", f"{expense:.2f}", f"{net:.2f}"))

    def plot_chart():
        nonlocal canvas  # to modify outer canvas variable

        # Clear previous canvas if exists
        if canvas is not None:
            canvas.get_tk_widget().destroy()

        daily_data = defaultdict(lambda: {"Income": 0.0, "Expense": 0.0})

        with open(manager.filename, 'r') as file:
            next(file)
            for line in file:
                date, category, txn_type, amount, _ = line.strip().split(',')
                amount = float(amount)
                if txn_type.lower() == 'income':
                    daily_data[date]["Income"] += amount
                elif txn_type.lower() == 'expense':
                    daily_data[date]["Expense"] += amount

        dates = sorted(daily_data.keys())
        income = [daily_data[d]["Income"] for d in dates]
        expense = [daily_data[d]["Expense"] for d in dates]

        fig, ax = plt.subplots(figsize=(7, 3), dpi=100)
        ax.bar(dates, income, label="Income", color='green')
        ax.bar(dates, expense, label="Expense", color='red', bottom=income)
        ax.set_ylabel("Amount")
        ax.set_title("Daily Income vs Expense")
        ax.legend()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=canvas_container)
        canvas.draw()
        canvas.get_tk_widget().pack()

    tb.Button(tab, text="Refresh Summary + Chart", command=lambda: [load_summary(), plot_chart()]).pack(pady=10)

    # Optionally, load data and chart on tab creation:
    load_summary()
    plot_chart()
