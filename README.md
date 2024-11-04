# Inventory Management System

A simple command-line inventory management system built with Python and SQLite. This application helps track products, manage stock levels, and monitor transactions.

## Features

- Add new products with initial quantity and price
- Manage stock levels (add/remove)
- View current inventory status
- Track all transactions (restocks and sales)
- SQLite database for persistent storage

## Project Structure

```
├── main.py           # Entry point and menu interface
├── database.py       # Database connection and setup
├── inventory.py      # Inventory management logic
└── inventory.db      # SQLite database (auto-generated)
```

## Requirements

- Python 3.x
- SQLite3 (included in Python standard library)

## Installation

1. Clone the repository or download the source code
2. No additional dependencies required

## Usage

Run the application using Python:

```bash
python3 main.py
```

### Menu Options

1. **Add Product**: Add a new product to inventory
2. **Add Stock**: Increase stock quantity for existing product
3. **Remove Stock**: Decrease stock quantity (for sales)
4. **View Inventory**: Display current stock levels
5. **View Transactions**: Show history of all transactions
6. **Exit**: Close the application

## Database Schema

### Products Table
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- quantity (INTEGER)
- price (REAL)

### Transactions Table
- id (INTEGER PRIMARY KEY)
- product_id (INTEGER, FOREIGN KEY)
- type (TEXT)
- quantity (INTEGER)
- date (TEXT)
