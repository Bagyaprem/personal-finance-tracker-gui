import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class User:
    def __init__(self, name, password, tpin, accno):
        self.name = name
        self.password = password
        self.tpin = tpin
        self.accno = accno

    def authenticate(self, input_name, input_password, input_tpin, input_accno):
        if (input_name == self.name and
            input_password == self.password and
            input_tpin == self.tpin and
            input_accno == self.accno):
            return True
        else:
            return False

class Account:
    def __init__(self, name, accno):
        self.name = name
        self.accno = accno
        self.balance_amount = 0  # Initialize balance amount to 0
        self.transactions = []   # List to store transaction objects

    def account_history(self):
        return self.transactions

    def process_transaction(self, transaction_type, amount, description):
        if transaction_type == "credit":
            self.balance_amount += amount
        elif transaction_type == "debit":
            if self.balance_amount >= amount:
                self.balance_amount -= amount
            else:
                messagebox.showerror("Error", "Insufficient balance.")
                return
        else:
            messagebox.showerror("Error", "Invalid transaction type.")
            return

        # Capture current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a Transaction object with timestamp and add it to transactions list
        transaction = Transaction(current_datetime, transaction_type, amount, description)
        self.transactions.append(transaction)
        messagebox.showinfo("Success", f"Transaction ({transaction_type}): Amount {amount} {transaction_type}ed successfully.")

    def display_balance(self):
        return self.balance_amount

class Transaction:
    def __init__(self, timestamp, transaction_type, amount, description):
        self.timestamp = timestamp
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description

    def __repr__(self):
        return f"{self.timestamp} - {self.transaction_type}: {self.amount} ({self.description})"

class Budget:
    def __init__(self, daily_limit):
        self.daily_limit = daily_limit

    def set_daily_limit(self, new_limit):
        self.daily_limit = new_limit
        messagebox.showinfo("Success", f"Daily budget limit updated to {self.daily_limit}.")

    def get_daily_limit(self):
        return self.daily_limit

def generate_financial_report(user_instance, account_instance, budget_instance):
    report = f"Financial Report\n\n"
    report += f"User Name: {user_instance.name}\n"
    report += f"Account Number: {user_instance.accno}\n"
    report += f"Daily Budget Limit: {budget_instance.get_daily_limit()}\n"
    report += f"Account Balance: {account_instance.display_balance()}\n"

    return report

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Application")

        # Initialize user and account objects
        self.user_instance = User("Prem", "2004", "1234", "6374005564")
        self.account_instance = Account("Prem", "6374005564")
        self.budget_instance = Budget(daily_limit=100000)

        # Create login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Enter your name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.login_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Enter your password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Enter your tpin:").grid(row=2, column=0, padx=10, pady=5)
        self.tpin_entry = tk.Entry(self.login_frame, show='*')
        self.tpin_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Enter your account number:").grid(row=3, column=0, padx=10, pady=5)
        self.accno_entry = tk.Entry(self.login_frame)
        self.accno_entry.grid(row=3, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.authenticate_user)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Create main frame for account operations
        self.main_frame = tk.Frame(self.root)

    def authenticate_user(self):
        input_name = self.name_entry.get()
        input_password = self.password_entry.get()
        input_tpin = self.tpin_entry.get()
        input_accno = self.accno_entry.get()

        if self.user_instance.authenticate(input_name, input_password, input_tpin, input_accno):
            messagebox.showinfo("Success", "Authentication successful! Go ahead.")
            self.login_frame.pack_forget()
            self.create_main_frame()
        else:
            messagebox.showerror("Error", "Authentication failed. Check your credentials.")

    def create_main_frame(self):
        self.main_frame.pack(pady=20)

        tk.Button(self.main_frame, text="View Account History", command=self.view_account_history).pack(pady=5)
        tk.Button(self.main_frame, text="Perform Transaction", command=self.perform_transaction).pack(pady=5)
        tk.Button(self.main_frame, text="View Account Balance", command=self.view_account_balance).pack(pady=5)
        tk.Button(self.main_frame, text="View Daily Budget Limit", command=self.view_daily_budget).pack(pady=5)
        tk.Button(self.main_frame, text="Generate Financial Report", command=self.generate_report).pack(pady=5)

    def view_account_history(self):
        transactions = self.account_instance.account_history()
        if not transactions:
            messagebox.showinfo("Account History", "No transactions yet.")
        else:
            history = "\n".join(str(transaction) for transaction in transactions)
            messagebox.showinfo("Account History", history)

    def perform_transaction(self):
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Perform Transaction")

        tk.Label(transaction_window, text="Enter transaction type (credit/debit):").grid(row=0, column=0, padx=10, pady=5)
        transaction_type_entry = tk.Entry(transaction_window)
        transaction_type_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(transaction_window, text="Enter amount:").grid(row=1, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(transaction_window)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(transaction_window, text="Enter transaction description:").grid(row=2, column=0, padx=10, pady=5)
        description_entry = tk.Entry(transaction_window)
        description_entry.grid(row=2, column=1, padx=10, pady=5)

        def submit_transaction():
            transaction_type = transaction_type_entry.get().lower()
            amount = float(amount_entry.get())
            description = description_entry.get()
            self.account_instance.process_transaction(transaction_type, amount, description)
            transaction_window.destroy()

        tk.Button(transaction_window, text="Submit", command=submit_transaction).grid(row=3, column=0, columnspan=2, pady=10)

    def view_account_balance(self):
        balance = self.account_instance.display_balance()
        messagebox.showinfo("Account Balance", f"Current Balance: {balance}")

    def view_daily_budget(self):
        daily_limit = self.budget_instance.get_daily_limit()
        messagebox.showinfo("Daily Budget Limit", f"Daily Budget Limit: {daily_limit}")

    def generate_report(self):
        report = generate_financial_report(self.user_instance, self.account_instance, self.budget_instance)
        messagebox.showinfo("Financial Report", report)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
