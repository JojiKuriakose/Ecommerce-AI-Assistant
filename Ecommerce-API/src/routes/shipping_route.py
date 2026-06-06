from fastapi import APIRouter, HTTPException, Query
from data.mock_ecommerce_data import SHIPPING_RATES, TRACKING_INFO

router = APIRouter(
    prefix="/shipping", 
    tags=["Shipping"],
)

# ============================================================================
# SHIPPING ENDPOINTS
# ============================================================================
@router.get("/shipping/rates")
async def get_shipping_rates(
    zip_code: str = Query(..., description="Destination ZIP code"),
    weight: float = Query(..., description="Package weight in pounds")
):
    """Get shipping rate estimates"""
    # Calculate rates (mock calculation)
    rates = []
    
    for rate_type, rate_info in SHIPPING_RATES.items():
        # Add small variation based on weight and zip
        base_cost = rate_info["cost"]
        weight_surcharge = max(0, (weight - 5) * 1.5)  # $1.5 per pound over 5 lbs
        
        total_cost = round(base_cost + weight_surcharge, 2)
        
        rates.append({
            "type": rate_type,
            "name": rate_info["name"],
            "cost": total_cost,
            "estimated_days": rate_info["days"],
            "carrier": "FastShip Logistics"
        })
    
    return {
        "destination": zip_code,
        "weight": weight,
        "rates": rates
    }


@router.get("/shipping/track/{tracking_number}")
async def track_shipment(tracking_number: str):
    """Track a shipment by tracking number"""
    if tracking_number not in TRACKING_INFO:
        raise HTTPException(status_code=404, detail="Tracking number not found")
    
    return TRACKING_INFO[tracking_number]


@router.post("/shipping/track")
async def track_shipment_post(tracking_number: str):
    """Track a shipment by tracking number (POST method)"""
    return await track_shipment(tracking_number)
