from fastapi import APIRouter, HTTPException
from typing import Optional
from data.mock_ecommerce_data import MOCK_ORDERS
from src.models.data_models import ProcessPaymentRequest

router= APIRouter(
    prefix="/payments",
    tags=["Payments"],
)
# ============================================================================
# PAYMENT ENDPOINTS
# ============================================================================

@router.post("/payments/process")
async def process_payment(request: ProcessPaymentRequest):
    """Process a payment (mock - always returns COD)"""
    order_id = request.order_id
    
    if order_id not in MOCK_ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Note: This is a mock API - real payments are handled offline
    return {
        "message": "Payment information recorded",
        "payment_method": "Cash on Delivery (COD)",
        "order_id": order_id,
        "amount": request.amount,
        "status": "pending",
        "note": "Payment will be collected upon delivery. This is a mock API - actual payments are handled offline."
    }


@router.post("/payments/{payment_id}/refund")
async def refund_payment(payment_id: str, amount: Optional[float] = None):
    """Process a refund (mock)"""
    return {
        "message": "Refund processed successfully",
        "payment_id": payment_id,
        "refund_amount": amount or 0.0,
        "status": "refunded",
        "note": "This is a mock refund. Actual refunds are handled through customer service."
    }
