import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('market.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        self.connection.commit()

    def add_product(self, name, price, quantity):
        try:
            self.cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            return False

    def fetch_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def remove_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            return False

    def __del__(self):
        self.connection.close()

class LoginWindow:
    def __init__(self, master, callback):
        self.master = master
        self.master.title("შესვლა")
        self.callback = callback
        self.setup_widgets()
        self.configure_styles()

    def setup_widgets(self):
        self.label_username = ttk.Label(self.master, text="მომხმარებლის სახელი:")
        self.entry_username = ttk.Entry(self.master, font=("Arial", 12))
        self.label_password = ttk.Label(self.master, text="პაროლი:")
        self.entry_password = ttk.Entry(self.master, show="*", font=("Arial", 12))
        self.btn_login = ttk.Button(self.master, text="შესვლა", command=self.login)

        # Layout
        self.label_username.grid(row=0, column=0, padx=10, pady=5)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.label_password.grid(row=1, column=0, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0", foreground="#333")
        style.configure("TButton", font=("Arial", 12), background="#E1E1E1", foreground="#333")
        style.configure("TEntry", font=("Arial", 12), foreground="#333")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "user2024" and password == "pass123":
            self.master.destroy()
            self.callback()
        else:
            self.print_message("არასწორი სახელი ან პაროლი")

    def print_message(self, message):
        messagebox.showinfo("Message", message)

class SupermarketManagementSystem:
    def __init__(self, master):
        self.master = master
        self.db = Database()
        self.setup_master()
        self.create_widgets()
        self.configure_styles()

    def setup_master(self):
        self.master.title("Supermarket Management System")
        self.master.geometry("500x350")

    def create_widgets(self):
        self.label_name = self.create_label("პროდუქტის სახელი:", 0)
        self.entry_name = self.create_entry(0)
        self.label_price = self.create_label("ფასი (GEL):", 1)
        self.entry_price = self.create_entry(1)
        self.label_quantity = self.create_label("რაოდენობა:", 2)
        self.entry_quantity = self.create_entry(2)

        self.btn_add = ttk.Button(self.master, text="დაამატე პროდუქტი", command=self.add_product)
        self.btn_show_products = ttk.Button(self.master, text="მარაგი", command=self.show_all_products)

        self.btn_add.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.btn_show_products.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def create_label(self, text, row):
        label = ttk.Label(self.master, text=text, font=("Arial", 12))
        label.grid(row=row, column=0, padx=10, pady=10, sticky="w")
        return label

    def create_entry(self, row):
        entry = ttk.Entry(self.master, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=10, pady=10)
        return entry

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0", foreground="#333")
        style.configure("TButton", font=("Arial", 12), background="#E1E1E1", foreground="#333")
        style.configure("TEntry", font=("Arial", 12), foreground="#333")

    def add_product(self):
        name = self.entry_name.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()

        if not name or not price or not quantity:
            self.print_message("შეავსეთ ყველა ველი")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            self.print_message("არასწორი ფასი ან რაოდენობა!")
            return

        if self.db.add_product(name, price, quantity):
            self.print_message("პროდუქტი წარმატებით დაემატა")
        else:
            self.print_message("პროდუქტი ვერ დაემატა")

        self.entry_name.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    def show_all_products(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("ყველა პროდუქტი")
        new_window.geometry("600x400")

        self.tree = ttk.Treeview(new_window, columns=("ID", "Name", "Price", "Quantity"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Quantity", text="Quantity")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Price", width=100)
        self.tree.column("Quantity", width=100)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(new_window, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.load_products_into_tree()

        # Add the "Remove" button
        btn_remove_product = ttk.Button(new_window, text="წაშალეთ პროდუქტი", command=self.remove_selected_product)
        btn_remove_product.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def load_products_into_tree(self):
        self.tree.delete(*self.tree.get_children())
        products = self.db.fetch_all_products()
        for product in products:
            self.tree.insert("", "end", values=product)

    def remove_selected_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.print_message("აირჩიეთ წასაშლელი პროდუქტი")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        if self.db.remove_product(product_id):
            self.print_message("პროდუქტი წარმატებით წაიშალა!")
            self.tree.delete(selected_item)
        else:
            self.print_message("პროდუქტი ვერ წაიშალა!!!")

    def print_message(self, message):
        messagebox.showinfo("Message", message)

if __name__ == "__main__":
    def launch_main_app():
        root = tk.Tk()
        app = SupermarketManagementSystem(root)
        root.mainloop()

    login_root = tk.Tk()
    login_app = LoginWindow(login_root, launch_main_app)
    login_root.mainloop()
