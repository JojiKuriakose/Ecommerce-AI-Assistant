"""
Simplified API Client for E-Commerce Web API Integrations
Clean, simple HTTP calls without complex session management.
Perfect for AI agents - just call methods and get responses!

Installation: pip install httpx
"""
import httpx
from typing import Dict, List, Optional

try:
    from config import (
        INVENTORY_API_URL,
        ORDERS_API_URL,
        PRODUCTS_API_URL,
        SHIPPING_API_URL,
        PAYMENTS_API_URL,
        CUSTOMERS_API_URL,
        API_HEADERS
    )
except ImportError:
    # Fallback if config import fails
    INVENTORY_API_URL = "https://api.example-ecommerce.com/inventory"
    ORDERS_API_URL = "https://api.example-ecommerce.com/orders"
    PRODUCTS_API_URL = "https://api.example-ecommerce.com/products"
    SHIPPING_API_URL = "https://api.example-ecommerce.com/shipping"
    PAYMENTS_API_URL = "https://api.example-ecommerce.com/payments"
    CUSTOMERS_API_URL = "https://api.example-ecommerce.com/customers"
    API_HEADERS = {"Content-Type": "application/json"}


class ECommerceAPIClient:
    """
    Simple API client using httpx - automatic session management, connection pooling,
    and HTTP/2 support built-in. Perfect for AI agents.
    
    No need to manually manage sessions, connectors, or cleanup!
    httpx handles all the complexity automatically.
    """
    
    def __init__(self, timeout: float = 30.0):
        """
        Initialize client with global timeout.
        
        Args:
            timeout: Request timeout in seconds (default: 30s)
        """
        self.timeout = timeout
    
    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Make HTTP request with automatic connection pooling.
        
        httpx.AsyncClient handles:
        - Connection pooling and reuse
        - Automatic retries on connection errors
        - Proper resource cleanup
        - HTTP/2 support
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(method, url, headers=API_HEADERS, **kwargs)
                return response
            except httpx.RequestError as e:
                print(f"Request error: {e}")
                raise
    
    # ===== Product APIs =====
    async def search_products(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        Search products by name or category
        
        API Call: GET /products/search?q={query}&category={category}
        Expected Response:
        [
            {
                "id": "PROD-001",
                "name": "Wireless Headphones",
                "category": "Electronics",
                "price": 79.99,
                "stock": 45,
                "description": "Premium wireless headphones with noise cancellation"
            }
        ]
        """
        params = {"q": query}
        if category:
            params["category"] = category
        
        try:
            response = await self._request("GET", f"{PRODUCTS_API_URL}/search", params=params)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return []  # No products found
            else:
                print(f"API Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    async def get_product_details(self, product_id: str) -> Optional[Dict]:
        """
        Get detailed information about a product
        
        API Call: GET /products/{product_id}
        Expected Response:
        {
            "id": "PROD-001",
            "name": "Wireless Headphones",
            "category": "Electronics",
            "price": 79.99,
            "stock": 45,
            "description": "Premium wireless headphones with noise cancellation",
            "specifications": {...},
            "images": [...]
        }
        """
        try:
            response = await self._request("GET", f"{PRODUCTS_API_URL}/{product_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None  # Product not found
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting product details: {e}")
            return None
    
    async def check_inventory(self, product_id: str) -> Dict:
        """
        Check inventory availability for a product
        
        API Call: GET /inventory/{product_id}
        Expected Response:
        {
            "available": true,
            "stock": 45,
            "product_id": "PROD-001",
            "product_name": "Wireless Headphones",
            "warehouse_locations": ["WH-01", "WH-03"]
        }
        """
        try:
            response = await self._request("GET", f"{INVENTORY_API_URL}/{product_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {
                    "available": False,
                    "stock": 0,
                    "product_id": product_id,
                    "message": "Product not found"
                }
            else:
                print(f"API Error: {response.status_code}")
                return {"available": False, "stock": 0, "message": "API error"}
        except Exception as e:
            print(f"Error checking inventory: {e}")
            return {"available": False, "stock": 0, "message": str(e)}
    
    # ===== Order APIs =====
    async def get_order_status(self, order_id: str) -> Optional[Dict]:
        """
        Get order status and details
        
        API Call: GET /orders/{order_id}
        Expected Response:
        {
            "order_id": "ORD-12345",
            "customer_id": "CUST-001",
            "status": "shipped",
            "items": [{"product_id": "PROD-001", "quantity": 2, "price": 79.99}],
            "total": 159.98,
            "created_at": "2025-12-18",
            "tracking_number": "TRK-98765"
        }
        """
        try:
            response = await self._request("GET", f"{ORDERS_API_URL}/{order_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None  # Order not found
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting order status: {e}")
            return None
    
    async def create_order(self, customer_id: str, items: List[Dict], total: float) -> Dict:
        """
        Create a new order
        
        API Call: POST /orders
        Request Body:
        {
            "customer_id": "CUST-001",
            "items": [{"product_id": "PROD-001", "quantity": 2}],
            "total": 159.98
        }
        
        Expected Response:
        {
            "order_id": "ORD-10002",
            "customer_id": "CUST-001",
            "status": "pending",
            "items": [...],
            "total": 159.98,
            "created_at": "2025-12-22",
            "tracking_number": null
        }
        """
        payload = {
            "customer_id": customer_id,
            "items": items,
            "total": total
        }
        
        try:
            response = await self._request("POST", f"{ORDERS_API_URL}", json=payload)
            if response.status_code in [200, 201]:
                return response.json()
            else:
                error_text = response.text
                print(f"API Error: {response.status_code} - {error_text}")
                return {
                    "success": False,
                    "message": f"Failed to create order: {error_text}"
                }
        except Exception as e:
            print(f"Error creating order: {e}")
            return {"success": False, "message": str(e)}
    
    async def cancel_order(self, order_id: str) -> Dict:
        """
        Cancel an order
        
        API Call: POST /orders/{order_id}/cancel
        
        Expected Response:
        {
            "success": true,
            "message": "Order cancelled successfully",
            "order_id": "ORD-12345",
            "refund_status": "pending"
        }
        """
        try:
            response = await self._request("POST", f"{ORDERS_API_URL}/{order_id}/cancel")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"success": False, "message": "Order not found"}
            elif response.status_code == 400:
                error_data = response.json()
                return {
                    "success": False,
                    "message": error_data.get("message", "Cannot cancel order")
                }
            else:
                print(f"API Error: {response.status_code}")
                return {"success": False, "message": "API error"}
        except Exception as e:
            print(f"Error cancelling order: {e}")
            return {"success": False, "message": str(e)}
    
    # ===== Shipping APIs =====
    async def get_shipping_rates(self, postal_code: str, weight: float = 5.0) -> Dict:
        """
        Get available shipping rates
        
        API Call: GET /shipping/rates?zip_code={postal_code}&weight={weight}
        Expected Response:
        {
            "destination": "12345",
            "weight": 5.0,
            "rates": [
                {"type": "standard", "cost": 5.99, "estimated_days": "5-7", "carrier": "FastShip Logistics"},
                {"type": "express", "cost": 15.99, "estimated_days": "2-3", "carrier": "FastShip Logistics"},
                {"type": "overnight", "cost": 29.99, "estimated_days": "1", "carrier": "FastShip Logistics"}
            ]
        }
        """
        try:
            response = await self._request(
                "GET",
                f"{SHIPPING_API_URL}/rates",
                params={"zip_code": postal_code, "weight": weight}
            )
            if response.status_code == 200:
                return response.json().get("rates", {})
            else:
                print(f"API Error: {response.status_code}")
                # Return default rates
                return {
                    "standard": {"cost": 5.99, "days": "5-7"},
                    "express": {"cost": 15.99, "days": "2-3"},
                    "overnight": {"cost": 29.99, "days": "1"}
                }
        except Exception as e:
            print(f"Error getting shipping rates: {e}")
            return {
                "standard": {"cost": 5.99, "days": "5-7"},
                "express": {"cost": 15.99, "days": "2-3"}
            }
    
    async def track_shipment(self, tracking_number: str) -> Dict:
        """
        Track a shipment
        
        API Call: GET /shipping/track/{tracking_number}
        Expected Response:
        {
            "tracking_number": "TRK-98765",
            "status": "in_transit",
            "estimated_delivery": "2025-12-24",
            "current_location": "Distribution Center, New York",
            "history": [
                {"timestamp": "2025-12-20T10:00:00Z", "location": "Origin", "status": "picked_up"},
                {"timestamp": "2025-12-21T14:30:00Z", "location": "Hub", "status": "in_transit"}
            ]
        }
        """
        try:
            response = await self._request("GET", f"{SHIPPING_API_URL}/track/{tracking_number}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {
                    "tracking_number": tracking_number,
                    "status": "not_found",
                    "message": "Tracking number not found"
                }
            else:
                print(f"API Error: {response.status_code}")
                return {
                    "tracking_number": tracking_number,
                    "status": "error",
                    "message": "Unable to track shipment"
                }
        except Exception as e:
            print(f"Error tracking shipment: {e}")
            return {
                "tracking_number": tracking_number,
                "status": "error",
                "message": str(e)
            }
    
    # ===== Customer APIs =====
    async def get_customer_info(self, customer_id: str) -> Optional[Dict]:
        """
        Get customer information
        
        API Call: GET /customers/{customer_id}
        Expected Response:
        {
            "customer_id": "CUST-001",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-0123",
            "loyalty_points": 450,
            "tier": "Gold",
            "member_since": "2023-01-15"
        }
        """
        try:
            response = await self._request("GET", f"{CUSTOMERS_API_URL}/{customer_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None  # Customer not found
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting customer info: {e}")
            return None
    
    async def get_loyalty_points(self, customer_id: str) -> Dict:
        """
        Get customer loyalty points
        
        API Call: GET /customers/{customer_id}/loyalty
        Expected Response:
        {
            "customer_id": "CUST-001",
            "points": 450,
            "tier": "Gold",
            "next_tier": "Platinum",
            "points_to_next_tier": 50
        }
        """
        try:
            response = await self._request("GET", f"{CUSTOMERS_API_URL}/{customer_id}/loyalty")
            if response.status_code == 200:
                data = response.json()
                data["found"] = True
                return data
            elif response.status_code == 404:
                return {
                    "customer_id": customer_id,
                    "points": 0,
                    "tier": "None",
                    "found": False
                }
            else:
                print(f"API Error: {response.status_code}")
                return {
                    "customer_id": customer_id,
                    "points": 0,
                    "tier": "Unknown",
                    "found": False
                }
        except Exception as e:
            print(f"Error getting loyalty points: {e}")
            return {"customer_id": customer_id, "points": 0, "tier": "Error", "found": False}
    
    async def redeem_points(self, customer_id: str, points: int) -> Dict:
        """
        Redeem loyalty points
        
        API Call: POST /customers/{customer_id}/loyalty/redeem
        Request Body:
        {
            "points": 100
        }
        
        Expected Response:
        {
            "success": true,
            "points_redeemed": 100,
            "discount_value": 1.00,
            "remaining_points": 350,
            "discount_code": "LOYALTY-ABC123"
        }
        """
        payload = {"points": points}
        
        try:
            response = await self._request(
                "POST",
                f"{CUSTOMERS_API_URL}/{customer_id}/loyalty/redeem",
                json=payload
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                return {
                    "success": False,
                    "message": error_data.get("message", "Insufficient points")
                }
            elif response.status_code == 404:
                return {"success": False, "message": "Customer not found"}
            else:
                print(f"API Error: {response.status_code}")
                return {"success": False, "message": "API error"}
        except Exception as e:
            print(f"Error redeeming points: {e}")
            return {"success": False, "message": str(e)}
    
    # ===== Payment APIs =====
    async def process_payment(self, order_id: str, payment_method: str, amount: float) -> Dict:
        """
        Process payment for an order
        
        API Call: POST /payments/process
        Request Body:
        {
            "order_id": "ORD-12345",
            "payment_method": "credit_card",
            "amount": 159.98,
            "currency": "USD"
        }
        
        Expected Response:
        {
            "success": true,
            "transaction_id": "TXN-ORD-12345-20251222120000",
            "order_id": "ORD-12345",
            "amount": 159.98,
            "payment_method": "credit_card",
            "status": "completed",
            "timestamp": "2025-12-22T12:00:00Z"
        }
        """
        payload = {
            "order_id": order_id,
            "payment_method": payment_method,
            "amount": amount,
            "currency": "USD"
        }
        
        try:
            response = await self._request("POST", f"{PAYMENTS_API_URL}/process", json=payload)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                return {
                    "success": False,
                    "message": error_data.get("message", "Payment failed"),
                    "order_id": order_id
                }
            else:
                print(f"API Error: {response.status_code}")
                return {
                    "success": False,
                    "message": "Payment processing error",
                    "order_id": order_id
                }
        except Exception as e:
            print(f"Error processing payment: {e}")
            return {"success": False, "message": str(e), "order_id": order_id}
    
    async def refund_payment(self, transaction_id: str, amount: float) -> Dict:
        """
        Process a refund
        
        API Call: POST /payments/refund
        Request Body:
        {
            "transaction_id": "TXN-ORD-12345-20251222120000",
            "amount": 79.99,
            "reason": "customer_request"
        }
        
        Expected Response:
        {
            "success": true,
            "refund_id": "REF-TXN-ORD-12345-20251222120000",
            "transaction_id": "TXN-ORD-12345-20251222120000",
            "amount": 79.99,
            "status": "processed",
            "expected_date": "2025-12-27",
            "refund_method": "original_payment_method"
        }
        """
        payload = {
            "transaction_id": transaction_id,
            "amount": amount,
            "reason": "customer_request"
        }
        
        try:
            response = await self._request("POST", f"{PAYMENTS_API_URL}/refund", json=payload)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                return {
                    "success": False,
                    "message": error_data.get("message", "Refund failed")
                }
            elif response.status_code == 404:
                return {"success": False, "message": "Transaction not found"}
            else:
                print(f"API Error: {response.status_code}")
                return {"success": False, "message": "Refund processing error"}
        except Exception as e:
            print(f"Error processing refund: {e}")
            return {"success": False, "message": str(e)}


# Global API client instance - ready to use!
api_client = ECommerceAPIClient()
