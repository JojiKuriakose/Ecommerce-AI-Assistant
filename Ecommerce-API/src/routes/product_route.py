from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from data.mock_ecommerce_data import MOCK_PRODUCTS

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

# ============================================================================
# PRODUCT ENDPOINTS
# ============================================================================

@router.get("/products/search")
async def search_products(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Search products by query and optional category"""
    results = []
    
    query_lower = q.lower()
    for product in MOCK_PRODUCTS.values():
        # Check if query matches name or description
        if (query_lower in product.name.lower() or 
            query_lower in product.description.lower() or
            query_lower in product.category.lower()):
            
            # Apply category filter if provided
            if category and product.category.lower() != category.lower():
                continue
            
            results.append(product.model_dump())
    
    return {
        "query": q,
        "category": category,
        "count": len(results),
        "results": results
    }


@router.get("/products/{product_id}")
async def get_product_details(product_id: str):
    """Get detailed information about a specific product"""
    if product_id not in MOCK_PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return MOCK_PRODUCTS[product_id].model_dump()


@router.get("/products/{product_id}/inventory")
async def check_inventory(product_id: str):
    """Check inventory availability for a product"""
    if product_id not in MOCK_PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = MOCK_PRODUCTS[product_id]
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "in_stock": product.in_stock,
        "quantity": product.stock_quantity,
        "availability": "Available" if product.in_stock else "Out of Stock",
        "restock_date": None if product.in_stock else "2025-01-15"
    }


@router.get("/products")
async def list_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    in_stock: Optional[bool] = Query(None, description="Filter by stock availability"),
    limit: int = Query(10, description="Maximum number of results")
):
    """List all products with optional filters"""
    results = list(MOCK_PRODUCTS.values())
    
    # Apply filters
    if category:
        results = [p for p in results if p.category.lower() == category.lower()]
    
    if in_stock is not None:
        results = [p for p in results if p.in_stock == in_stock]
    
    # Apply limit
    results = results[:limit]
    
    return {
        "count": len(results),
        "products": [p.model_dump() for p in results]
    }
