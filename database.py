import sqlite3

def init_db():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    
    # Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    
    # Insert initial sample data if table is empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Wireless Mechanical Keyboard", 89.99),
            ("Ultra-Wide Monitor 34\"", 499.99),
            ("Developer Ergonomic Chair", 299.99),
            ("Noise Cancelling Headphones", 199.99)
        ]
        cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", sample_products)
        conn.commit()
        
    conn.close()

def get_all_products():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products")
    rows = cursor.fetchall()
    conn.close()
    
    return [{"id": row[0], "name": row[1], "price": row[2]} for row in rows]

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")