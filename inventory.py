from datetime import datetime

class InventoryManager:
    def __init__(self, db):
        self.db = db

    def add_product(self, name, quantity, price):
        self.db.cursor.execute('''
            INSERT INTO products (name, quantity, price)
            VALUES (?, ?, ?)
        ''', (name, quantity, price))
        self.db.conn.commit()
        print(f"Added product: {name}")

    def update_quantity(self, product_id, quantity_change, transaction_type):
        self.db.cursor.execute('SELECT quantity FROM products WHERE id = ?', (product_id,))
        current_quantity = self.db.cursor.fetchone()[0]
        new_quantity = current_quantity + quantity_change

        if new_quantity < 0:
            print("Error: Not enough stock")
            return False

        self.db.cursor.execute('''
            UPDATE products 
            SET quantity = ?
            WHERE id = ?
        ''', (new_quantity, product_id))

        self.db.cursor.execute('''
            INSERT INTO transactions (product_id, type, quantity, date)
            VALUES (?, ?, ?, ?)
        ''', (product_id, transaction_type, quantity_change, datetime.now().isoformat()))

        self.db.conn.commit()
        return True

    def view_inventory(self):
        self.db.cursor.execute('SELECT * FROM products')
        products = self.db.cursor.fetchall()
        
        print("\nCurrent Inventory:")
        print("ID | Name | Quantity | Price")
        print("-" * 30)
        for product in products:
            print(f"{product[0]} | {product[1]} | {product[2]} | ${product[3]:.2f}")

    def view_transactions(self):
        self.db.cursor.execute('''
            SELECT t.id, p.name, t.type, t.quantity, t.date
            FROM transactions t
            JOIN products p ON t.product_id = p.id
        ''')
        transactions = self.db.cursor.fetchall()
        
        print("\nTransaction History:")
        print("ID | Product | Type | Quantity | Date")
        print("-" * 50)
        for trans in transactions:
            print(f"{trans[0]} | {trans[1]} | {trans[2]} | {trans[3]} | {trans[4]}")