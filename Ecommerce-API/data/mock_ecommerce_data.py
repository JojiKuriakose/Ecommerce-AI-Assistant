from datetime import datetime, timedelta
from src.models.data_models import Product, Order, OrderItem, ShippingAddress, Customer

MOCK_PRODUCTS = {
    "PROD-001": Product(
        id="PROD-001",
        name="Wireless Bluetooth Headphones",
        category="Electronics",
        price=79.99,
        description="Premium wireless headphones with noise cancellation",
        in_stock=True,
        stock_quantity=45,
        rating=4.5,
        image_url="https://example.com/headphones.jpg"
    ),
    "PROD-002": Product(
        id="PROD-002",
        name="Laptop Stand Aluminum",
        category="Accessories",
        price=39.99,
        description="Ergonomic aluminum laptop stand",
        in_stock=True,
        stock_quantity=120,
        rating=4.7,
        image_url="https://example.com/stand.jpg"
    ),
    "PROD-003": Product(
        id="PROD-003",
        name="USB-C Hub Adapter",
        category="Electronics",
        price=29.99,
        description="7-in-1 USB-C hub with HDMI and USB ports",
        in_stock=True,
        stock_quantity=200,
        rating=4.3,
        image_url="https://example.com/hub.jpg"
    ),
    "PROD-004": Product(
        id="PROD-004",
        name="Mechanical Keyboard RGB",
        category="Electronics",
        price=129.99,
        description="Gaming mechanical keyboard with RGB lighting",
        in_stock=False,
        stock_quantity=0,
        rating=4.8,
        image_url="https://example.com/keyboard.jpg"
    ),
    "PROD-005": Product(
        id="PROD-005",
        name="Wireless Mouse",
        category="Electronics",
        price=24.99,
        description="Ergonomic wireless mouse with programmable buttons",
        in_stock=True,
        stock_quantity=85,
        rating=4.4,
        image_url="https://example.com/mouse.jpg"
    ),
}

MOCK_ORDERS = {
    "ORD-12345": Order(
        id="ORD-12345",
        customer_id="CUST-001",
        items=[
            OrderItem(
                product_id="PROD-001",
                product_name="Wireless Bluetooth Headphones",
                quantity=1,
                price=79.99
            )
        ],
        total_amount=79.99,
        status="shipped",
        shipping_address=ShippingAddress(
            street="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
            country="USA"
        ),
        tracking_number="TRK-789456123",
        created_at=datetime.now() - timedelta(days=3),
        updated_at=datetime.now() - timedelta(hours=12)
    ),
    "ORD-67890": Order(
        id="ORD-67890",
        customer_id="CUST-002",
        items=[
            OrderItem(
                product_id="PROD-002",
                product_name="Laptop Stand Aluminum",
                quantity=2,
                price=39.99
            )
        ],
        total_amount=79.98,
        status="processing",
        shipping_address=ShippingAddress(
            street="456 Oak Ave",
            city="Los Angeles",
            state="CA",
            zip_code="90001",
            country="USA"
        ),
        tracking_number=None,
        created_at=datetime.now() - timedelta(days=1),
        updated_at=datetime.now() - timedelta(hours=2)
    ),
}

MOCK_CUSTOMERS = {
    "CUST-001": Customer(
        id="CUST-001",
        name="John Doe",
        email="john.doe@example.com",
        phone="+1-555-0123",
        loyalty_points=2500,
        member_since=datetime(2023, 1, 15)
    ),
    "CUST-002": Customer(
        id="CUST-002",
        name="Jane Smith",
        email="jane.smith@example.com",
        phone="+1-555-0456",
        loyalty_points=1200,
        member_since=datetime(2023, 6, 20)
    ),
}

SHIPPING_RATES = {
    "standard": {"name": "Standard Shipping", "cost": 5.99, "days": "5-7"},
    "express": {"name": "Express Shipping", "cost": 15.99, "days": "2-3"},
    "overnight": {"name": "Overnight Shipping", "cost": 29.99, "days": "1"},
}

TRACKING_INFO = {
    "TRK-789456123": {
        "tracking_number": "TRK-789456123",
        "status": "in_transit",
        "current_location": "Distribution Center - Chicago, IL",
        "estimated_delivery": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "history": [
            {"timestamp": "2025-12-25 08:00", "location": "Origin - New York, NY", "status": "Picked up"},
            {"timestamp": "2025-12-26 14:30", "location": "Distribution Center - Chicago, IL", "status": "In transit"},
        ]
    },
    "TRK-123456789": {
        "tracking_number": "TRK-123456789",
        "status": "delivered",
        "current_location": "Delivered",
        "estimated_delivery": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "history": [
            {"timestamp": "2025-12-20 09:00", "location": "Origin - Los Angeles, CA", "status": "Picked up"},
            {"timestamp": "2025-12-21 16:45", "location": "Distribution Center - Phoenix, AZ", "status": "In transit"},
            {"timestamp": "2025-12-22 11:30", "location": "Local Facility - San Diego, CA", "status": "Out for delivery"},
            {"timestamp": "2025-12-22 15:20", "location": "San Diego, CA", "status": "Delivered"},
        ]
    },
}
