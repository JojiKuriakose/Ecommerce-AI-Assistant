"""Agents package for E-Commerce multi-agent system"""
from .product_agent import ProductAgent
from .order_agent import OrderAgent
from .shipping_agent import ShippingAgent
from .customer_agent import CustomerAgent

__all__ = [
    'ProductAgent',
    'OrderAgent',
    'ShippingAgent',
    'CustomerAgent'
]
