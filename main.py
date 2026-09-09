from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

products_db = [
    {"id": 1, "name": "Wireless Mechanical Keyboard", "price": 89.99},
    {"id": 2, "name": "Ultra-Wide Monitor 34\"", "price": 499.99},
    {"id": 3, "name": "Developer Ergonomic Chair", "price": 299.99}
]

@app.get("/api/products")
def get_products():
    return products_db