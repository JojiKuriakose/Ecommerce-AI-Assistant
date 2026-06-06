from datetime import datetime
from fastapi import APIRouter

router=APIRouter(
    prefix="",
    tags=["Root"],
)
# ============================================================================
# ROOT & HEALTH ENDPOINTS
# ============================================================================
@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "E-Commerce Mock API",
        "version": "1.0.0",
        "endpoints": {
            "products": "/products",
            "orders": "/orders",
            "shipping": "/shipping",
            "customers": "/customers",
            "payments": "/payments"
        },
        "docs": "/docs"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "E-Commerce Mock API"
    }
