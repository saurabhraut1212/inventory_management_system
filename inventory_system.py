import sqlite3
import os
from datetime import datetime

class InventorySystem:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        self.conn.commit()

    def add_product(self, name, quantity, price):
        self.cursor.execute('''
            INSERT INTO products (name, quantity, price)
            VALUES (?, ?, ?)
        ''', (name, quantity, price))
        self.conn.commit()
        print(f"Added product: {name}")

    def update_quantity(self, product_id, quantity_change, transaction_type):
        self.cursor.execute('SELECT quantity FROM products WHERE id = ?', (product_id,))
        current_quantity = self.cursor.fetchone()[0]
        new_quantity = current_quantity + quantity_change

        if new_quantity < 0:
            print("Error: Not enough stock")
            return False

        self.cursor.execute('''
            UPDATE products 
            SET quantity = ?
            WHERE id = ?
        ''', (new_quantity, product_id))

        self.cursor.execute('''
            INSERT INTO transactions (product_id, type, quantity, date)
            VALUES (?, ?, ?, ?)
        ''', (product_id, transaction_type, quantity_change, datetime.now().isoformat()))

        self.conn.commit()
        return True

    def view_inventory(self):
        self.cursor.execute('SELECT * FROM products')
        products = self.cursor.fetchall()
        
        print("\nCurrent Inventory:")
        print("ID | Name | Quantity | Price")
        print("-" * 30)
        for product in products:
            print(f"{product[0]} | {product[1]} | {product[2]} | ${product[3]:.2f}")

    def view_transactions(self):
        self.cursor.execute('''
            SELECT t.id, p.name, t.type, t.quantity, t.date
            FROM transactions t
            JOIN products p ON t.product_id = p.id
        ''')
        transactions = self.cursor.fetchall()
        
        print("\nTransaction History:")
        print("ID | Product | Type | Quantity | Date")
        print("-" * 50)
        for trans in transactions:
            print(f"{trans[0]} | {trans[1]} | {trans[2]} | {trans[3]} | {trans[4]}")

    def close(self):
        self.conn.close()

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    inventory = InventorySystem()

    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Add Stock")
        print("3. Remove Stock")
        print("4. View Inventory")
        print("5. View Transactions")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            name = input("Enter product name: ")
            quantity = int(input("Enter initial quantity: "))
            price = float(input("Enter price: "))
            inventory.add_product(name, quantity, price)

        elif choice == '2':
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity to add: "))
            inventory.update_quantity(product_id, quantity, "RESTOCK")

        elif choice == '3':
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity to remove: "))
            inventory.update_quantity(product_id, -quantity, "SALE")

        elif choice == '4':
            inventory.view_inventory()

        elif choice == '5':
            inventory.view_transactions()

        elif choice == '6':
            inventory.close()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()