"""
E-Commerce REST API Server
===========================

Mock REST APIs for:
- Products (search, details, inventory)
- Orders (status, create, cancel)
- Shipping (rates, tracking)
- Customers (info, loyalty points)
- Payments (process, refund)

Run with: uvicorn ecommerce_apis.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.root_health_route import router as root_health_route
from src.routes.product_route import router as product_route
from src.routes.order_route import router as order_route
from src.routes.shipping_route import router as shipping_route
from src.routes.customer_route import router as customer_route
from src.routes.payment_route import router as payment_route

app = FastAPI(
    title="E-Commerce Mock API",
    description="Mock REST APIs for e-commerce multi-agent system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_health_route)
app.include_router(product_route)
app.include_router(order_route)
app.include_router(shipping_route)
app.include_router(customer_route)
app.include_router(payment_route)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 70)
    print("  E-Commerce Mock API Server")
    print("=" * 70)
    print("\n📡 Starting server on http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🔧 Alternative docs: http://localhost:8000/redoc")
    print("\n" + "=" * 70 + "\n")
    
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        log_level="info"
    )
