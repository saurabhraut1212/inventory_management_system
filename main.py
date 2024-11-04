import os
from database import Database
from inventory import InventoryManager

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    db = Database()
    inventory = InventoryManager(db)

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
            db.close()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()