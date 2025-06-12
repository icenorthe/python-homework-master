# app/dto/product_dto.py

from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class ProductDto:
    title: str
    price: Decimal
    description: Optional[str]
    status: str
    user_id: int
