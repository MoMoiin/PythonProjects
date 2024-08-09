import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sv_ttk
import csv
import os
import uuid


# Create the main application window
win = tk.Tk()

# Change Title
win.title("Income/Expense List")

# Set the window icon
win.iconbitmap(
    "Icon/calculator-icon_34473.ico"
)  # Ensure the icon file is in the same directory or provide the full path


# Set the minimum width of the window
win.minsize(width=1100, height=400)  # Adjust the width and height as needed

# Set the transparency level of the window
win.attributes("-alpha", 0.98)  # 0.9 means 90% opaque, 10% transparent

# Apply the sv_ttk theme
sv_ttk.set_theme("dark")  # Options are "dark" and "light"

# Create a main content frame
main_content = ttk.Frame(win)
main_content.pack(expand=True, fill="both")

# Create a frame for input fields and buttons
input_frame = ttk.Frame(main_content)
input_frame.pack(side="left", fill="y", padx=10, pady=10)

# Define a fixed width for the entry fields
entry_width = 30

# Add input fields and buttons for expenses and income
expense_label = ttk.Label(input_frame, text="Expense:", font=("Segoe UI", 12))
expense_label.pack(pady=5)
expense_entry = ttk.Entry(input_frame, width=entry_width)
expense_entry.pack(pady=5)

income_label = ttk.Label(input_frame, text="Income:", font=("Segoe UI", 12))
income_label.pack(pady=5)
income_entry = ttk.Entry(input_frame, width=entry_width)
income_entry.pack(pady=5)

# Add a date entry field
date_label = ttk.Label(input_frame, text="Date (DD-MM-YY):", font=("Segoe UI", 12))
date_label.pack(pady=5)
current_date = datetime.now().strftime("%d-%m-%y")
date_entry = ttk.Entry(input_frame, width=entry_width)
date_entry.insert(0, current_date)
date_entry.pack(pady=5)

# Add a text entry for the description
description_label = ttk.Label(input_frame, text="Description:", font=("Segoe UI", 12))
description_label.pack(pady=5)
description_entry = ttk.Entry(input_frame, width=entry_width)
description_entry.pack(pady=5)

# Add a dropdown menu to select between Expense and Income
transaction_type = tk.StringVar(value="Expense")
transaction_menu = ttk.OptionMenu(
    input_frame, transaction_type, "Expense", "Expense", "Income"
)
transaction_menu.config(width=entry_width - 2)  # Adjust width to match entry fields
transaction_menu.pack(pady=5)

# Add a dropdown menu to select the month
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
selected_month = tk.StringVar(value=datetime.now().strftime("%B"))
month_menu = ttk.OptionMenu(input_frame, selected_month, *months)
month_menu.config(width=entry_width - 2)  # Adjust width to match entry fields
month_menu.pack(pady=5)

# Initialize total expense, income, and balance
total_expense = 0
total_income = 0
balance = 0


def get_data_file():
    return f"transactions_{selected_month.get()}.csv"


def validate_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def save_data():
    # Get the input values
    expense = expense_entry.get()
    income = income_entry.get()
    date = date_entry.get()
    transaction = transaction_type.get()
    description = description_entry.get()

    # Validate inputs
    if not validate_number(expense) and not validate_number(income):
        messagebox.showerror(
            "Input Error", "Please enter a valid number for expense or income."
        )
        return
    if not date:
        messagebox.showerror("Input Error", "Please enter a date.")
        return

    data_file = get_data_file()
    with open(data_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Generate a unique ID for the new entry
        new_id = str(uuid.uuid4())
        writer.writerow([new_id, expense, income, date, transaction, description])

    # Clear the input fields
    expense_entry.delete(0, tk.END)
    income_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, current_date)
    description_entry.delete(0, tk.END)
    load_data()  # Refresh the data display


def load_data():
    global total_expense, total_income
    total_expense = 0
    total_income = 0
    data_file = get_data_file()
    for row in tree.get_children():
        tree.delete(row)
    if os.path.exists(data_file):
        with open(data_file, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", tk.END, values=row)
                if len(row) == 6:
                    _, expense, income, date, transaction, description = row
                else:
                    _, expense, income, date, transaction = row
                    description = ""  # Default to an empty description if not present
                if validate_number(expense):
                    total_expense += float(expense)
                if validate_number(income):
                    total_income += float(income)
    update_total_label()


def update_total_label():
    total_label.config(
        text=f"Total Expense: ${total_expense:.2f}, Total Income: ${total_income:.2f}"
    )


def delete_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Selection Error", "Please select items to delete.")
        return
    selected_ids = [tree.item(item, "values")[0] for item in selected_items]
    data_file = get_data_file()
    with open(data_file, mode="r") as file:
        rows = list(csv.reader(file))
    with open(data_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] not in selected_ids:
                writer.writerow(row)
    load_data()


# Create a frame for displaying the data
display_frame = ttk.Frame(main_content)
display_frame.pack(side="top", fill="both", expand=True, padx=10, pady=30)

# Create a Treeview widget to display the data
columns = ("ID", "Expense", "Income", "Date", "Type", "Description")
tree = ttk.Treeview(display_frame, columns=columns, show="headings")
for col in columns[1:]:  # Skip the ID column
    tree.heading(col, text=col)
tree.pack(side="left", expand=True, fill="both")

# Hide the ID column
tree.column("ID", width=0, stretch=tk.NO)

# Create a vertical scrollbar for the Treeview
scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")

# Configure the Treeview to use the scrollbar
tree.configure(yscrollcommand=scrollbar.set)

# Create a frame for buttons and totals under the Treeview
button_frame = ttk.Frame(main_content)
button_frame.pack(side="bottom", fill="x", pady=20)

# Add a save button
save_button = ttk.Button(button_frame, text="Save", command=save_data)
save_button.pack(side="left", padx=5)

# Add delete button
delete_button = ttk.Button(button_frame, text="Delete", command=delete_selected)
delete_button.pack(side="left", padx=5)

# Add a label to display the total expenses and income for the selected month
total_label = ttk.Label(button_frame, text="Total: $0.00", font=("Segoe UI", 12))
total_label.pack(side="left", padx=5)

# Load data when the selected month changes
selected_month.trace("w", lambda *args: load_data())

# Load data on startup
load_data()

# Start the main event loop
win.mainloop()
