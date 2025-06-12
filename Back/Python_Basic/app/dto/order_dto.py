# app/dto/order_dto.py

from dataclasses import dataclass
from typing import List, Optional
from app.models.order import Order
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.user import User

@dataclass
class OrderDto(Order):
    product: Optional[Product] = None
    images: Optional[List[ProductImage]] = None
    buyer: Optional[User] = None
    seller: Optional[User] = None
