from pydantic import (
    BaseModel,
    Field,
    AnyUrl,
    field_validator,
    model_validator,
    computed_field,
    EmailStr,
)
from typing import Annotated, Literal, Optional, List, Dict
from uuid import UUID
from datetime import datetime


# A class for adding Dimensions Validation
class Dimensions(BaseModel):
    length: Annotated[float, Field(gt=0, strict=True, description="Length in cm")]
    width: Annotated[float, Field(gt=0, description="Width in cm")]
    height: Annotated[float, Field(gt=0, description="Width in cm")]


# Creating a class for seller_details
class Seller(BaseModel):
    id: UUID  # Generates a default unique UUID
    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=60,
            title="Seller Name",
            description="Name of the seller",
            examples=["Mi Store", "Official Realme"],
        ),
    ]
    email: EmailStr
    website: AnyUrl

    @field_validator("email", mode="after")
    @classmethod
    def validate_seller_email_domain(cls, value: EmailStr):
        allowed_domains = [
            "mistore.in",
            "hpworld.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
            "applestoreindia.in",
            "dellexclusive.in",
            "sonycenter.in",
            "oneplusstore.in",
            "asusexlusive.in",
        ]
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"Seller email domain not allowed: {domain}")
        return value


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
    price: Annotated[float, Field(gt=0, description="Base price in INR")]
    currency: Literal["INR"] = "INR"
    discount_percent: Annotated[
        int, Field(ge=0, le=90, description="Discount in percent (0-90)")
    ] = 0
    stock: Annotated[int, Field(ge=0, description="Available stock units(>=0)")]
    is_active: Annotated[bool, Field(description="Is product active")]
    rating: Annotated[float, Field(ge=0, le=5, description="Product rating (0-5)")]
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

    dimensions_cm: Dimensions
    seller: Seller
    created_at: datetime

    # Using validators to check the format of specific fields
    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value: str):
        if "-" not in value:
            raise ValueError("sku must contain a '-'")

        last = value.split("-")[-1]
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("sku must end with a 3-digit sequence like -012")

        return value

    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, then is_active must be false")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError(
                "Discounted price must have a few ratings. (ie rating != 0)"
            )

        return model

    @computed_field
    @property
    def finalPrice(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)

    @computed_field
    @property
    def volume_cm3(self) -> float:
        d = self.dimensions_cm
        return round(d.length * d.width * d.height)