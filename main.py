from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Instancia de la aplicación FastAPI
app = FastAPI()

# Base de datos simulada
fake_db = {
    1: {"name": "Laptop", "price": 1000},
    2: {"name": "Phone", "price": 500},
    3: {"name": "Tablet", "price": 400},
    4: {"name": "Headphones", "price": 200},
}

# Pydantic models (para validar la entrada)
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tax: Optional[float] = None

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API con FastAPI"}

# Endpoint para obtener todos los productos
@app.get("/products")
def get_products():
    return fake_db

# Endpoint para obtener un producto por ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in fake_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return fake_db[product_id]

# Endpoint para crear un nuevo producto
@app.post("/products/")
def create_product(item: Item):
    product_id = len(fake_db) + 1
    fake_db[product_id] = item.dict()
    return {"msg": "Producto creado", "product_id": product_id}

# Endpoint para actualizar un producto
@app.put("/products/{product_id}")
def update_product(product_id: int, item: Item):
    if product_id not in fake_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    fake_db[product_id] = item.dict()
    return {"msg": "Producto actualizado", "product_id": product_id}

# Endpoint para eliminar un producto
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in fake_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    del fake_db[product_id]
    return {"msg": "Producto eliminado", "product_id": product_id}
