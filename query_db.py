import sqlite3

DB_NAME = "ecommerce.db"

def run_query(query, params=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Helper search functions ---
def get_products():
    return run_query("SELECT * FROM products;")

def get_customers():
    return run_query("SELECT * FROM customers;")

def get_transactions():
    return run_query("SELECT * FROM transactions;")

def find_product_by_name(name):
    return run_query("SELECT * FROM products WHERE name LIKE ?;", (f"%{name}%",))

def products_below_stock(threshold):
    return run_query("SELECT * FROM products WHERE stock < ?;", (threshold,))

def find_customer_by_email(email):
    return run_query("SELECT * FROM customers WHERE email = ?;", (email,))

def get_customer_transactions(customer_id):
    query = """
        SELECT 
            c.name AS customer_name,
            c.email AS customer_email,
            p.name AS product_name,
            p.price AS product_price,
            t.quantity,
            t.timestamp
        FROM transactions t
        JOIN customers c ON t.customer_id = c.id
        JOIN products p ON t.product_id = p.id
        WHERE c.id = ?
        ORDER BY t.timestamp DESC;
    """
    return run_query(query, (customer_id,))

def get_customer_summary(customer_id):
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
    return run_query(query, (customer_id,))

if __name__ == "__main__":
    print("All Products:")
    for row in get_products():
        print(row)

    print("\n All Customers:")
    for row in get_customers():
        print(row)

    print("\n All Transactions:")
    for row in get_transactions():
        print(row)

    print("\n Search Product by Name ('Mouse'):")
    for row in find_product_by_name("Mouse"):
        print(row)

    print("\n Products below stock 10:")
    for row in products_below_stock(10):
        print(row)

    print("\n Find Customer by Email ('alice@example.com'):")
    for row in find_customer_by_email("alice@example.com"):
        print(row)

    print("\n Transaction history for Alice (cust1):")
    for row in get_customer_transactions("cust1"):
        print(row)

    print("\n Purchase summary for Alice (cust1):")
    for row in get_customer_summary("cust1"):
        print(row)
