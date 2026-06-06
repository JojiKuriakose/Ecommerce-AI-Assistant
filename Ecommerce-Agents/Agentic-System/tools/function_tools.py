"""
Function Tools Definitions for E-Commerce Agents
These tools will be called by Azure AI Foundry agents
"""
import json
import asyncio
from typing import Dict, Any, Set, Callable
from api.api_client_simple import api_client

# ===== Product Agent Tools =====
SEARCH_PRODUCTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_products",
        "description": "Search for products by keyword or category in the e-commerce catalog",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (product name or keyword)"
                },
                "category": {
                    "type": "string",
                    "description": "Filter by product category (optional)",
                    "enum": ["Electronics", "Sports", "Home", "Clothing"]
                }
            },
            "required": ["query"]
        }
    }
}

GET_PRODUCT_DETAILS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_product_details",
        "description": "Get detailed information about a specific product",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "The unique product ID"
                }
            },
            "required": ["product_id"]
        }
    }
}

CHECK_INVENTORY_TOOL = {
    "type": "function",
    "function": {
        "name": "check_inventory",
        "description": "Check if a product is in stock and available",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "The product ID to check inventory for"
                }
            },
            "required": ["product_id"]
        }
    }
}

# ===== Order Agent Tools =====
GET_ORDER_STATUS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_order_status",
        "description": "Get the current status and details of an order",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to check"
                }
            },
            "required": ["order_id"]
        }
    }
}

CREATE_ORDER_TOOL = {
    "type": "function",
    "function": {
        "name": "create_order",
        "description": "Create a new order for a customer",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID placing the order"
                },
                "items": {
                    "type": "string",
                    "description": "JSON string of items array with product_id and quantity"
                },
                "total": {
                    "type": "number",
                    "description": "Total order amount"
                }
            },
            "required": ["customer_id", "items", "total"]
        }
    }
}

CANCEL_ORDER_TOOL = {
    "type": "function",
    "function": {
        "name": "cancel_order",
        "description": "Cancel an existing order",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID to cancel"
                }
            },
            "required": ["order_id"]
        }
    }
}

# ===== Shipping Agent Tools =====
GET_SHIPPING_RATES_TOOL = {
    "type": "function",
    "function": {
        "name": "get_shipping_rates",
        "description": "Get available shipping rates and delivery times for a shipment",
        "parameters": {
            "type": "object",
            "properties": {
                "postal_code": {
                    "type": "string",
                    "description": "Destination postal code"
                },
                "weight": {
                    "type": "number",
                    "description": "Package weight in pounds (default: 5.0)"
                }
            },
            "required": ["postal_code"]
        }
    }
}

TRACK_SHIPMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "track_shipment",
        "description": "Track a shipment using tracking number",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_number": {
                    "type": "string",
                    "description": "The shipment tracking number"
                }
            },
            "required": ["tracking_number"]
        }
    }
}

# ===== Customer Agent Tools =====
GET_CUSTOMER_INFO_TOOL = {
    "type": "function",
    "function": {
        "name": "get_customer_info",
        "description": "Get customer account information",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                }
            },
            "required": ["customer_id"]
        }
    }
}

GET_LOYALTY_POINTS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_loyalty_points",
        "description": "Get customer loyalty points balance",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                }
            },
            "required": ["customer_id"]
        }
    }
}

REDEEM_POINTS_TOOL = {
    "type": "function",
    "function": {
        "name": "redeem_points",
        "description": "Redeem loyalty points for discount",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID"
                },
                "points": {
                    "type": "integer",
                    "description": "Number of points to redeem"
                }
            },
            "required": ["customer_id", "points"]
        }
    }
}

# Note: Payment is handled offline/COD - no payment agent needed


# ===== Function Executor =====
async def execute_function(function_name: str, arguments: Dict[str, Any]) -> str:
    """
    Execute the appropriate API call based on function name
    This is called by agents when they need to use tools
    """
    try:
        # Product functions
        if function_name == "search_products":
            results = await api_client.search_products(
                query=arguments.get("query", ""),
                category=arguments.get("category")
            )
            return json.dumps(results, indent=2)
        
        elif function_name == "get_product_details":
            result = await api_client.get_product_details(arguments.get("product_id", ""))
            return json.dumps(result, indent=2) if result else "Product not found"
        
        elif function_name == "check_inventory":
            result = await api_client.check_inventory(arguments.get("product_id", ""))
            return json.dumps(result, indent=2)
        
        # Order functions
        elif function_name == "get_order_status":
            result = await api_client.get_order_status(arguments.get("order_id", ""))
            return json.dumps(result, indent=2) if result else "Order not found"
        
        elif function_name == "create_order":
            items = json.loads(arguments.get("items", "[]"))
            result = await api_client.create_order(
                customer_id=arguments.get("customer_id", ""),
                items=items,
                total=arguments.get("total", 0.0)
            )
            return json.dumps(result, indent=2)
        
        elif function_name == "cancel_order":
            result = await api_client.cancel_order(arguments.get("order_id", ""))
            return json.dumps(result, indent=2)
        
        # Shipping functions
        elif function_name == "get_shipping_rates":
            result = await api_client.get_shipping_rates(
                arguments.get("postal_code", ""),
                arguments.get("weight", 5.0)
            )
            return json.dumps(result, indent=2)
        
        elif function_name == "track_shipment":
            result = await api_client.track_shipment(arguments.get("tracking_number", ""))
            return json.dumps(result, indent=2)
        
        # Customer functions
        elif function_name == "get_customer_info":
            result = await api_client.get_customer_info(arguments.get("customer_id", ""))
            return json.dumps(result, indent=2) if result else "Customer not found"
        
        elif function_name == "get_loyalty_points":
            result = await api_client.get_loyalty_points(arguments.get("customer_id", ""))
            return json.dumps(result, indent=2)
        
        elif function_name == "redeem_points":
            result = await api_client.redeem_points(
                customer_id=arguments.get("customer_id", ""),
                points=arguments.get("points", 0)
            )
            return json.dumps(result, indent=2)
        
        else:
            return f"Unknown function: {function_name}"
    
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"


# ===== Callable Functions for FunctionTool =====
# These are synchronous wrappers that the SDK's FunctionTool can execute

def _run_async(coro):
    """Helper to run async code synchronously"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a new loop
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


def search_products(query: str, category: str = None) -> str:
    """
    Search for products by keyword or category in the e-commerce catalog.
    
    :param query: Search query (product name or keyword)
    :param category: Filter by product category (optional). Values: Electronics, Sports, Home, Clothing
    :return: JSON string of matching products
    """
    result = _run_async(api_client.search_products(query=query, category=category))
    return json.dumps(result, indent=2)


def get_product_details(product_id: str) -> str:
    """
    Get detailed information about a specific product.
    
    :param product_id: The unique product ID
    :return: JSON string of product details
    """
    result = _run_async(api_client.get_product_details(product_id))
    return json.dumps(result, indent=2) if result else "Product not found"


def check_inventory(product_id: str) -> str:
    """
    Check if a product is in stock and available.
    
    :param product_id: The product ID to check inventory for
    :return: JSON string of inventory status
    """
    result = _run_async(api_client.check_inventory(product_id))
    return json.dumps(result, indent=2)


def get_order_status(order_id: str) -> str:
    """
    Get the current status and details of an order.
    
    :param order_id: The order ID to check
    :return: JSON string of order status
    """
    result = _run_async(api_client.get_order_status(order_id))
    return json.dumps(result, indent=2) if result else "Order not found"


def create_order(customer_id: str, items: str, total: float) -> str:
    """
    Create a new order for a customer.
    
    :param customer_id: The customer ID placing the order
    :param items: JSON string of items array with product_id and quantity
    :param total: Total order amount
    :return: JSON string of created order
    """
    items_list = json.loads(items) if isinstance(items, str) else items
    result = _run_async(api_client.create_order(customer_id=customer_id, items=items_list, total=total))
    return json.dumps(result, indent=2)


def cancel_order(order_id: str) -> str:
    """
    Cancel an existing order.
    
    :param order_id: The order ID to cancel
    :return: JSON string of cancellation result
    """
    result = _run_async(api_client.cancel_order(order_id))
    return json.dumps(result, indent=2)


def get_shipping_rates(postal_code: str, weight: float = 5.0) -> str:
    """
    Get available shipping rates and delivery times for a shipment.
    
    :param postal_code: Destination postal code
    :param weight: Package weight in pounds (default: 5.0)
    :return: JSON string of shipping rates
    """
    result = _run_async(api_client.get_shipping_rates(postal_code, weight))
    return json.dumps(result, indent=2)


def track_shipment(tracking_number: str) -> str:
    """
    Track a shipment using tracking number.
    
    :param tracking_number: The shipment tracking number
    :return: JSON string of tracking information
    """
    result = _run_async(api_client.track_shipment(tracking_number))
    return json.dumps(result, indent=2)


def get_customer_info(customer_id: str) -> str:
    """
    Get customer account information.
    
    :param customer_id: The customer ID
    :return: JSON string of customer information
    """
    result = _run_async(api_client.get_customer_info(customer_id))
    return json.dumps(result, indent=2) if result else "Customer not found"


def get_loyalty_points(customer_id: str) -> str:
    """
    Get customer loyalty points balance.
    
    :param customer_id: The customer ID
    :return: JSON string of loyalty points
    """
    result = _run_async(api_client.get_loyalty_points(customer_id))
    return json.dumps(result, indent=2)


def redeem_points(customer_id: str, points: int) -> str:
    """
    Redeem loyalty points for discount.
    
    :param customer_id: The customer ID
    :param points: Number of points to redeem
    :return: JSON string of redemption result
    """
    result = _run_async(api_client.redeem_points(customer_id=customer_id, points=points))
    return json.dumps(result, indent=2)


# Map of function names to callable functions
CALLABLE_FUNCTIONS = {
    "search_products": search_products,
    "get_product_details": get_product_details,
    "check_inventory": check_inventory,
    "get_order_status": get_order_status,
    "create_order": create_order,
    "cancel_order": cancel_order,
    "get_shipping_rates": get_shipping_rates,
    "track_shipment": track_shipment,
    "get_customer_info": get_customer_info,
    "get_loyalty_points": get_loyalty_points,
    "redeem_points": redeem_points,
}


def get_callable_functions(tool_names: list) -> Set[Callable]:
    """
    Get a set of callable functions for the given tool names.
    Used by FunctionTool in the new SDK.
    
    :param tool_names: List of function names to get
    :return: Set of callable functions
    """
    funcs = set()
    for name in tool_names:
        if name in CALLABLE_FUNCTIONS:
            funcs.add(CALLABLE_FUNCTIONS[name])
    return funcs


__all__ = ["execute_function", "get_callable_functions"]
