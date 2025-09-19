import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# --- Create tables ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

# --- Insert sample data ---
cursor.executemany(
    "INSERT OR IGNORE INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
    [
        ("p1", "Wireless Mouse", 25.99, 50),
        ("p2", "Mouse Pad", 7.99, 100),
        ("p3", "Mechanical Keyboard", 55.00, 20),
        ("p4", "USB-C Cable", 9.99, 75),
        ("p5", "Webcam", 35.50, 30),
    ]
)

cursor.executemany(
    "INSERT OR IGNORE INTO customers (id, name, email) VALUES (?, ?, ?)",
    [
        ("cust1", "Alice", "alice@example.com"),
        ("cust2", "Bob", "bob@example.com"),
        ("cust3", "Charlie", "charlie@example.com"),
    ]
)

cursor.executemany(
    "INSERT INTO transactions (customer_id, product_id, quantity) VALUES (?, ?, ?)",
    [
        ("cust1", "p1", 1),
        ("cust1", "p2", 2),
        ("cust2", "p3", 1),
        ("cust2", "p4", 3),
        ("cust3", "p5", 1),
    ]
)

conn.commit()
conn.close()

print("Database initialized successfully 🚀 (with stock column).")
