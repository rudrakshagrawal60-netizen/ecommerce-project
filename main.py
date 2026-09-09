from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def setup_database():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
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

# Start hote hi database ban jayega
setup_database()

@app.get("/api/products")
def get_products():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "price": r[2]} for r in rows]