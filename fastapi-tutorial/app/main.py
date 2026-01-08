from fastapi import FastAPI, HTTPException, Query, Path
from app.service.products import (
    get_all_products,
    load_products,
    add_product,
    remove_product,
)
from app.schema.productSchema import Product
from uuid import uuid4, UUID
from datetime import datetime


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI."}


@app.get("/all")
def all_products():
    load_products()


@app.get("/products")
def list_products(
    name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Search by product name (case insensitive)",
    ),
    limit: int = Query(default=10, ge=1, le=100),
):

    products = get_all_products()

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
        raise HTTPException(
            status_code=404, detail=f"No product found with name {name}"
        )

    total = len(products)

    return {"total": total, "items": products}


@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: str = Path(
        default=...,
        min_length=36,
        max_length=36,
        description="UUID for the product",
        example="24a9d4f3-d78c-4a1e-b516-5c50c46fc1be",
    )
):
    products = get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", status_code=201)
def create_products(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product.model_dump(mode="json")


@app.delete("/products/{product_id}")
def delete_product(
    product_id: UUID = Path(..., description="Product UUID")
):
    try:
        data = remove_product(str(product_id))
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

