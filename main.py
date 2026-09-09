from fastapi import FastAPI
from pydantic import BaseModel
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
class ProductSchema(BaseModel):
    name: str
    price: float

# Naya product add karne ke liye API
@app.post("/api/products")
def add_product(product: ProductSchema):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (product.name, product.price))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "name": product.name, "price": product.price}

# Product delete karne ke liye API
@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return {"message": "Product deleted successfully"}
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from jose import jwt
SECRET_KEY = "your-secret-key-for-jwt"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password Hashing Helpers
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token Creation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Admin Auth Schemas
class AuthSchema(BaseModel):
    username: str
    password: str

# Admin Login Endpoint
@app.post("/api/login")
def login(data: AuthSchema):
    # Default Admin Credentials
    if data.username == "admin" and data.password == "admin123":
        token = create_access_token({"sub": data.username})
        return {"access_token": token, "token_type": "bearer"}
    return {"error": "Invalid credentials"}
class OrderSchema(BaseModel):
    customer_name: str
    amount: float
    items: str

# Orders Table Setup
def setup_orders_table():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            amount REAL NOT NULL,
            items TEXT NOT NULL,
            status TEXT DEFAULT 'Paid'
        )
    """)
    conn.commit()
    conn.close()

setup_orders_table()

# Create Order API
@app.post("/api/orders")
def create_order(order: OrderSchema):
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_name, amount, items) VALUES (?, ?, ?)",
                   (order.customer_name, order.amount, order.items))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return {"id": order_id, "status": "Success"}

# Get Orders List (Admin View)
@app.get("/api/orders")
def get_orders():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_name, amount, items, status FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "customer": r[1], "amount": r[2], "items": r[3], "status": r[4]} for r in rows]