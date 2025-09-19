import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# --- Create tables ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    total REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

# --- Seed sample data ---
products = [
    ("Laptop", 75000, 10),
    ("Smartphone", 35000, 25),
    ("Headphones", 5000, 50),
]

customers = [
    ("Alice Johnson", "alice@example.com"),
    ("Bob Smith", "bob@example.com"),
    ("Charlie Brown", "charlie@example.com"),
]

transactions = [
    (1, 1, 1, 75000),   # Alice buys a Laptop
    (2, 2, 2, 70000),   # Bob buys 2 Smartphones
    (3, 3, 3, 15000),   # Charlie buys 3 Headphones
]

cursor.executemany("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", products)
cursor.executemany("INSERT INTO customers (name, email) VALUES (?, ?)", customers)
cursor.executemany("INSERT INTO transactions (customer_id, product_id, quantity, total) VALUES (?, ?, ?, ?)", transactions)

# Save changes and close
conn.commit()
conn.close()

print("Database seeded successfully 🚀")
