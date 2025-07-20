import ttkbootstrap as tb
import os

def create_view_tab(tab_control, manager):
    tab = tb.Frame(tab_control)
    tab_control.add(tab, text='📄 View Transactions')

    # Create Treeview with columns
    tree = tb.Treeview(tab, columns=("Date", "Category", "Type", "Amount", "Description"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        anchor = 'e' if col == 'Amount' else 'center'  # Right-align Amount, center others
        tree.column(col, anchor=anchor, width=120)
    tree.pack(side='left', expand=True, fill='both')

    # Add vertical scrollbar
    scrollbar = tb.Scrollbar(tab, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    def load_transactions():
        tree.delete(*tree.get_children())

        if not os.path.exists(manager.filename):
            return  # File doesn't exist, nothing to load

        with open(manager.filename, 'r') as file:
            next(file, None)  # Skip header line if present
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                parts = line.split(',')
                if len(parts) < 5:
                    continue  # Skip malformed lines
                tree.insert('', 'end', values=parts)

    # Load transactions automatically when this tab is selected
    def on_tab_changed(event):
        selected_tab = event.widget.select()
        if event.widget.nametowidget(selected_tab) == tab:
            load_transactions()

    tab_control.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Don't load transactions here on creation to avoid redundant loading

    # Removed Refresh button to prevent manual reload
    # tb.Button(tab, text="Refresh", command=load_transactions).pack(pady=10)

    return tab
