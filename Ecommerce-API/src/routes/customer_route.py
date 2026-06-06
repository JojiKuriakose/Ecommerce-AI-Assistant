from fastapi import APIRouter, HTTPException
from data.mock_ecommerce_data import MOCK_CUSTOMERS
from src.models.data_models import RedeemPointsRequest

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

# ============================================================================
# CUSTOMER ENDPOINTS
# ============================================================================


@router.get("/customers/{customer_id}")
async def get_customer_info(customer_id: str):
    """Get customer account information"""
    if customer_id not in MOCK_CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return MOCK_CUSTOMERS[customer_id].model_dump()


@router.get("/customers/{customer_id}/loyalty")
async def get_loyalty_points(customer_id: str):
    """Get customer loyalty points balance"""
    if customer_id not in MOCK_CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer = MOCK_CUSTOMERS[customer_id]
    
    return {
        "customer_id": customer_id,
        "customer_name": customer.name,
        "loyalty_points": customer.loyalty_points,
        "tier": "Gold" if customer.loyalty_points > 2000 else "Silver" if customer.loyalty_points > 1000 else "Bronze",
        "points_to_next_tier": max(0, 1000 - (customer.loyalty_points % 1000)) if customer.loyalty_points < 2000 else 0,
        "rewards_value": round(customer.loyalty_points * 0.01, 2)  # 1 point = $0.01
    }


@router.post("/customers/{customer_id}/loyalty/redeem")
async def redeem_loyalty_points(customer_id: str, request: RedeemPointsRequest):
    """Redeem customer loyalty points"""
    if customer_id not in MOCK_CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer = MOCK_CUSTOMERS[customer_id]
    points = request.points
    
    if points <= 0:
        raise HTTPException(status_code=400, detail="Points must be greater than 0")
    
    if customer.loyalty_points < points:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient points. Available: {customer.loyalty_points}, Requested: {points}"
        )
    
    # Redeem points
    customer.loyalty_points -= points
    discount_value = round(points * 0.01, 2)  # 1 point = $0.01
    
    return {
        "message": "Points redeemed successfully",
        "customer_id": customer_id,
        "points_redeemed": points,
        "discount_value": discount_value,
        "remaining_points": customer.loyalty_points
    }
