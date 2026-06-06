"""
Order Agent - Handles order creation, status, and cancellation
"""
from .base_agent import FoundryBaseAgent
from tools.function_tools import (
    GET_ORDER_STATUS_TOOL,
    CREATE_ORDER_TOOL,
    CANCEL_ORDER_TOOL
)


class OrderAgent(FoundryBaseAgent):
    """Agent specialized in order management"""
    
    def __init__(self, project_endpoint: str, model_deployment: str):
        instructions = """You are an Order Management Specialist for an e-commerce platform.

Your responsibilities:
- Check order status and provide tracking information
- Help customers place new orders
- Process order cancellations when requested
- Provide order history and details

IMPORTANT: All orders use Cash on Delivery (COD) or offline payment. 
When creating orders, inform customers that payment will be collected upon delivery.

Use the available tools to access real-time order data from our API.
Be professional, efficient, and ensure customers understand their order status."""

        tools = [
            GET_ORDER_STATUS_TOOL,
            CREATE_ORDER_TOOL,
            CANCEL_ORDER_TOOL
        ]
        
        super().__init__(
            name="OrderAgent",
            instructions=instructions,
            tools=tools,
            project_endpoint=project_endpoint,
            model_deployment=model_deployment
        )
    
    # def can_handle(self, query: str) -> bool:
    #     """Check if this agent can handle the query"""
    #     keywords = [
    #         "order", "purchase", "buy", "status", "tracking",
    #         "cancel", "place order", "create order", "my order"
    #     ]
    #     return any(keyword in query.lower() for keyword in keywords)
