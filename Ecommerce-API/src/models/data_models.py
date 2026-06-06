# ============================================================================
# DATA MODELS
# ============================================================================
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    description: str
    in_stock: bool
    stock_quantity: int
    rating: float
    image_url: Optional[str] = None


class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float


class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class Order(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItem]
    total_amount: float
    status: str
    shipping_address: ShippingAddress
    tracking_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class Customer(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    loyalty_points: int
    member_since: datetime


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[dict]
    shipping_address: dict


class RedeemPointsRequest(BaseModel):
    customer_id: str
    points: int


class ProcessPaymentRequest(BaseModel):
    order_id: str
    payment_method: str
    amount: float
