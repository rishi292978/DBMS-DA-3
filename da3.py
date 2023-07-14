import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a database connection
conn = sqlite3.connect("billing_system.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        item_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        FOREIGN KEY (item_id) REFERENCES items(id)
    )
""")
conn.commit()


class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")

        # Create login page
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

        # Create main page
        self.main_frame = tk.Frame(self.root)
        self.bill_button = tk.Button(self.main_frame, text="Billing", command=self.show_billing_page)
        self.bill_button.pack()

        self.history_button = tk.Button(self.main_frame, text="Transaction History", command=self.show_history_page)
        self.history_button.pack()

        self.database_button = tk.Button(self.main_frame, text="Database", command=self.show_database_page)
        self.database_button.pack()

        self.logout_button = tk.Button(self.main_frame, text="Logout", command=self.logout)
        self.logout_button.pack()

        # Create billing page
        self.billing_frame = tk.Frame(self.root)

        self.item_label = tk.Label(self.billing_frame, text="Item:")
        self.item_label.pack()
        self.item_entry = tk.Entry(self.billing_frame)
        self.item_entry.pack()

        self.quantity_label = tk.Label(self.billing_frame, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.billing_frame)
        self.quantity_entry.pack()

        self.bill_button = tk.Button(self.billing_frame, text="Bill", command=self.bill)
        self.bill_button.pack()

        self.back_button = tk.Button(self.billing_frame, text="Back", command=self.show_main_page)
        self.back_button.pack()

        # Create transaction history page
        self.history_frame = tk.Frame(self.root)

        self.history_text = tk.Text(self.history_frame)
        self.history_text.pack()

        self.back_button = tk.Button(self.history_frame, text="Back", command=self.show_main_page)
        self.back_button.pack()

        # Create database page
        self.database_frame = tk.Frame(self.root)

        self.add_button = tk.Button(self.database_frame, text="Add Item", command=self.add_item_window)
        self.add_button.pack()

        self.delete_button = tk.Button(self.database_frame, text="Delete Item", command=self.delete_item_window)
        self.delete_button.pack()

        self.update_button = tk.Button(self.database_frame, text="Update Item", command=self.update_item_window)
        self.update_button.pack()

        self.back_button = tk.Button(self.database_frame, text="Back", command=self.show_main_page)
        self.back_button.pack()

        self.show_login_page()

    def show_login_page(self):
        self.main_frame.pack_forget()
        self.billing_frame.pack_forget()
        self.history_frame.pack_forget()
        self.database_frame.pack_forget()
        self.login_frame.pack()

    def show_main_page(self):
        self.login_frame.pack_forget()
        self.billing_frame.pack_forget()
        self.history_frame.pack_forget()
        self.database_frame.pack_forget()
        self.main_frame.pack()

    def show_billing_page(self):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.history_frame.pack_forget()
        self.database_frame.pack_forget()
        self.billing_frame.pack()

    def show_history_page(self):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.billing_frame.pack_forget()
        self.database_frame.pack_forget()
        self.history_frame.pack()
        self.load_transaction_history()

    def show_database_page(self):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.billing_frame.pack_forget()
        self.history_frame.pack_forget()
        self.database_frame.pack()

    def load_transaction_history(self):
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()

        self.history_text.delete("1.0", tk.END)
        for transaction in transactions:
            self.history_text.insert(tk.END, f"Transaction ID: {transaction[0]}\n")
            self.history_text.insert(tk.END, f"Item ID: {transaction[1]}\n")
            self.history_text.insert(tk.END, f"Quantity: {transaction[2]}\n")
            self.history_text.insert(tk.END, f"Total Price: {transaction[3]}\n")
            self.history_text.insert(tk.END, "------------------------\n")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Perform your login authentication here
        # Replace this with your actual login logic

        if username == "admin" and password == "password":
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.show_main_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def logout(self):
        self.show_login_page()

    def bill(self):
        item_name = self.item_entry.get()
        quantity = int(self.quantity_entry.get())

        cursor.execute("SELECT id, price FROM items WHERE name=?", (item_name,))
        item = cursor.fetchone()

        if item:
            item_id, price = item
            total_price = price * quantity

            cursor.execute("INSERT INTO transactions (item_id, quantity, total_price) VALUES (?, ?, ?)",
                           (item_id, quantity, total_price))
            conn.commit()

            messagebox.showinfo("Success", "Billing successful")
            self.item_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid item")

    def add_item_window(self):
        add_item_window = tk.Toplevel(self.root)
        add_item_window.title("Add Item")

        name_label = tk.Label(add_item_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(add_item_window)
        name_entry.pack()

        price_label = tk.Label(add_item_window, text="Price:")
        price_label.pack()
        price_entry = tk.Entry(add_item_window)
        price_entry.pack()

        add_button = tk.Button(add_item_window, text="Add", command=lambda: self.add_item(add_item_window, name_entry.get(), price_entry.get()))
        add_button.pack()

    def add_item(self, add_item_window, name, price):
        if name and price:
            try:
                price = float(price)
                cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
                conn.commit()

                messagebox.showinfo("Success", "Item added")
                add_item_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid price")
        else:
            messagebox.showerror("Error", "Name and price are required")

    def delete_item_window(self):
        delete_item_window = tk.Toplevel(self.root)
        delete_item_window.title("Delete Item")

        id_label = tk.Label(delete_item_window, text="Item ID:")
        id_label.pack()
        id_entry = tk.Entry(delete_item_window)
        id_entry.pack()

        delete_button = tk.Button(delete_item_window, text="Delete", command=lambda: self.delete_item(delete_item_window, id_entry.get()))
        delete_button.pack()

    def delete_item(self, delete_item_window, item_id):
        if item_id:
            try:
                item_id = int(item_id)
                cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
                conn.commit()

                messagebox.showinfo("Success", "Item deleted")
                delete_item_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid item ID")
        else:
            messagebox.showerror("Error", "Item ID is required")

    def update_item_window(self):
        update_item_window = tk.Toplevel(self.root)
        update_item_window.title("Update Item")

        id_label = tk.Label(update_item_window, text="Item ID:")
        id_label.pack()
        id_entry = tk.Entry(update_item_window)
        id_entry.pack()

        price_label = tk.Label(update_item_window, text="New Price:")
        price_label.pack()
        price_entry = tk.Entry(update_item_window)
        price_entry.pack()

        update_button = tk.Button(update_item_window, text="Update", command=lambda: self.update_item(update_item_window, id_entry.get(), price_entry.get()))
        update_button.pack()

    def update_item(self, update_item_window, item_id, new_price):
        if item_id and new_price:
            try:
                item_id = int(item_id)
                new_price = float(new_price)
                cursor.execute("UPDATE items SET price=? WHERE id=?", (new_price, item_id))
                conn.commit()

                messagebox.showinfo("Success", "Item updated")
                update_item_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid item ID or price")
        else:
            messagebox.showerror("Error", "Item ID and new price are required")


if __name__ == "__main__":
    root = tk.Tk()
    BillingSystem(root)
    root.mainloop()