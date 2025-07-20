import ttkbootstrap as tb
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np  # Add numpy for bar positioning

def create_summary_tab(tab_control, manager):
    tab = tb.Frame(tab_control)
    tab_control.add(tab, text='📊 Daily Summary')

    # Frame for the Refresh button on top
    btn_frame = tb.Frame(tab)
    btn_frame.pack(fill='x', pady=10)

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

        x = np.arange(len(dates))
        width = 0.35

        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)

        bars_income = ax.bar(x - width/2, income, width, label='Income', color='green')
        bars_expense = ax.bar(x + width/2, expense, width, label='Expense', color='red')

        ax.set_ylabel('Amount')
        ax.set_title('Daily Income vs Expense')
        ax.set_xticks(x)
        ax.set_xticklabels(dates, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8)

        autolabel(bars_income)
        autolabel(bars_expense)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=canvas_container)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Add styled refresh button on top
    refresh_btn = tb.Button(btn_frame, text="Refresh Summary + Chart", bootstyle="success-outline", command=lambda: [load_summary(), plot_chart()])
    refresh_btn.pack(padx=10, pady=5, anchor='w')

    # Load data & chart initially
    load_summary()
    plot_chart()
