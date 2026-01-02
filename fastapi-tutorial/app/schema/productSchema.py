from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated, Literal, Optional, List, Dict
from uuid import UUID
from datetime import datetime


# Creating class for "POST" to add new product in products
class Product(BaseModel):
    id: UUID  # Generates a default unique UUID
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="SKU",
            description="Stock Keeping Unit",
            examples=["1234-abc-567-8d"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Relatable product name",
            examples=["Poco X6 Pro, MacBook M4, ASUS Vivobook 16x"],
        ),
    ]
    description: Annotated[
        str,
        Field(max_length=200, description="Information that describes your product"),
    ]
    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="The category in which your product fits",
            examples=["Electronics", "Entertainment", "Accessories", "Home"],
        ),
    ]
    brand: Annotated[
        str, Field(min_length=2, max_length=20, examples=["Asus", "Samsumg", "Apple"])
    ]
    price: Annotated[float, Field(gt=0, strict=True, description="Base price in INR")]
    currency: Literal["INR"] = "INR"
    discount_percent: Annotated[
        int, Field(ge=0, le=90, description="Discount in percent (0-90)")
    ] = 0
    stock: Annotated[int, Field(ge=0, description="Available stock units(>=0)")]
    is_active: Annotated[bool, Field(description="Is product active")]
    rating: Annotated[
        float, Field(ge=0, le=5, strict=True, description="Product rating (0-5)")
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(
            description="Add tags that define your product",
            default=None,
            max_length=10,
            examples=["Electronic", "Smartphone", "Kids", "Toys"],
        ),
    ]
    image_urls: Annotated[
        List[AnyUrl],
        Field(min_length=1, description="Atleast 1 image URL", max_length=10),
    ]

    # dimensions_cm
    # seller
    created_at: datetime
