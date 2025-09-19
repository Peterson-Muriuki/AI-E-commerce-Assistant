from fastapi import FastAPI
import sqlite3

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("ecommerce.db")
    conn.row_factory = sqlite3.Row  # return dict-like rows
    return conn

@app.get("/")
def root():
    return {"message": "AI E-commerce Assistant - API with SQLite running"}

# --- Existing endpoints ---
@app.get("/products")
def list_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(row) for row in products]

@app.get("/customers")
def list_customers():
    conn = get_db_connection()
    customers = conn.execute("SELECT * FROM customers").fetchall()
    conn.close()
    return [dict(row) for row in customers]

@app.get("/transactions")
def list_transactions():
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return [dict(row) for row in transactions]

# --- New endpoint: Customer Summary ---
@app.get("/customers/{customer_id}/summary")
def customer_summary(customer_id: str):
    conn = get_db_connection()
    query = """
        SELECT 
            c.name AS customer_name,
            c.email AS customer_email,
            COUNT(t.id) AS total_orders,
            SUM(t.quantity) AS total_items,
            SUM(t.quantity * p.price) AS total_spent
        FROM transactions t
        JOIN customers c ON t.customer_id = c.id
        JOIN products p ON t.product_id = p.id
        WHERE c.id = ?
        GROUP BY c.id, c.name, c.email;
    """
    result = conn.execute(query, (customer_id,)).fetchone()
    conn.close()

    if result:
        return dict(result)
    else:
        return {"error": f"No summary found for customer_id {customer_id}"}

# --- New endpoint: Customer Transactions (Purchase History) ---
@app.get("/customers/{customer_id}/transactions")
def customer_transactions(customer_id: str):
    conn = get_db_connection()
    query = """
        SELECT 
            t.id AS transaction_id,
            t.timestamp,
            p.name AS product_name,
            p.price,
            t.quantity,
            (t.quantity * p.price) AS total_price
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        WHERE t.customer_id = ?
        ORDER BY t.timestamp DESC;
    """
    results = conn.execute(query, (customer_id,)).fetchall()
    conn.close()

    return [dict(row) for row in results] if results else {"error": f"No transactions found for customer_id {customer_id}"}
