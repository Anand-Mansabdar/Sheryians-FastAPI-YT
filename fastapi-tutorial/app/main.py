from fastapi import FastAPI, HTTPException, Query, Path
from service.products import get_all_products, load_products
from pydantic import BaseModel, Field
from typing import Annotated

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


# Creating class for "POST" to add new product in products
class Product(BaseModel):
    id: str
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="SKU",
            description="Stock Keeping Unit",
            examples=["1234-abc-567-8d"],
        ),
    ]  # Annotation of the field "sku". Tells that field sku must pass through all the above validations
    name: str = "New Product"  # Setting a default value to a product


@app.post("/products", status_code=201)
def create_products(product: Product):
    return product
