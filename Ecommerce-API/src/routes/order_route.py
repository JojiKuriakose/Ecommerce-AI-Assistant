from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from data.mock_ecommerce_data import MOCK_ORDERS, MOCK_CUSTOMERS, MOCK_PRODUCTS
from src.models.data_models import Order, OrderItem, ShippingAddress, CreateOrderRequest
import uuid

router = APIRouter(
    prefix="/orders",   
    tags=["Orders"],
)

# ============================================================================
# ORDER ENDPOINTS
# ============================================================================

@router.get("/orders/{order_id}")
async def get_order_status(order_id: str):
    """Get order status and details"""
    if order_id not in MOCK_ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return MOCK_ORDERS[order_id].model_dump()


@router.post("/orders")
async def create_order(request: CreateOrderRequest):
    """Create a new order"""
    # Validate customer
    if request.customer_id not in MOCK_CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Generate order ID
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    # Process items
    order_items = []
    total_amount = 0.0
    
    for item in request.items:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)
        
        if product_id not in MOCK_PRODUCTS:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        
        product = MOCK_PRODUCTS[product_id]
        
        if not product.in_stock or product.stock_quantity < quantity:
            raise HTTPException(status_code=400, detail=f"Product {product_id} not available in requested quantity")
        
        order_items.append(OrderItem(
            product_id=product_id,
            product_name=product.name,
            quantity=quantity,
            price=product.price
        ))
        
        total_amount += product.price * quantity
    
    # Create order
    new_order = Order(
        id=order_id,
        customer_id=request.customer_id,
        items=order_items,
        total_amount=round(total_amount, 2),
        status="pending",
        shipping_address=ShippingAddress(**request.shipping_address),
        tracking_number=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    MOCK_ORDERS[order_id] = new_order
    
    return {
        "message": "Order created successfully",
        "order": new_order.model_dump()
    }


@router.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: str, reason: Optional[str] = None):
    """Cancel an existing order"""
    if order_id not in MOCK_ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = MOCK_ORDERS[order_id]
    
    # Check if order can be cancelled
    if order.status in ["shipped", "delivered", "cancelled"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel order with status: {order.status}"
        )
    
    # Update order status
    order.status = "cancelled"
    order.updated_at = datetime.now()
    
    return {
        "message": "Order cancelled successfully",
        "order_id": order_id,
        "status": "cancelled",
        "reason": reason or "Customer request"
    }


@router.get("/orders")
async def list_orders(
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(10, description="Maximum number of results")
):
    """List orders with optional filters"""
    results = list(MOCK_ORDERS.values())
    
    # Apply filters
    if customer_id:
        results = [o for o in results if o.customer_id == customer_id]
    
    if status:
        results = [o for o in results if o.status.lower() == status.lower()]
    
    # Apply limit
    results = results[:limit]
    
    return {
        "count": len(results),
        "orders": [o.model_dump() for o in results]
    }
