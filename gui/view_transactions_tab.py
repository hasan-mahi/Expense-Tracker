# gui/view_transactions_tab.py

import ttkbootstrap as tb

def create_view_tab(tab_control, manager):
    tab = tb.Frame(tab_control)
    tab_control.add(tab, text='📄 View Transactions')

    tree = tb.Treeview(tab, columns=("Date", "Category", "Type", "Amount", "Description"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=120)
    tree.pack(expand=True, fill='both')

    def load_transactions():
        tree.delete(*tree.get_children())
        with open(manager.filename, 'r') as file:
            next(file)
            for line in file:
                tree.insert('', 'end', values=line.strip().split(','))

    tb.Button(tab, text="Refresh", command=load_transactions).pack(pady=10)
