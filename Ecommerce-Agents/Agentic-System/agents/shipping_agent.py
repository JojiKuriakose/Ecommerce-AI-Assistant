"""
Shipping Agent - Handles shipping rates and tracking
"""
from .base_agent import FoundryBaseAgent
from tools.function_tools import (
    GET_SHIPPING_RATES_TOOL,
    TRACK_SHIPMENT_TOOL
)


class ShippingAgent(FoundryBaseAgent):
    """Agent specialized in shipping and delivery"""
    
    def __init__(self, project_endpoint: str, model_deployment: str):
        instructions = """You are a Shipping and Delivery Specialist for an e-commerce platform.

Your responsibilities:
- Provide shipping rate information for different delivery methods
- Track shipments and provide delivery status updates
- Explain shipping options (standard, express, overnight)
- Help customers understand delivery timelines

Use the available tools to access real-time shipping data from our API.
Be clear about delivery times and costs.
Help customers choose the best shipping option for their needs."""

        tools = [
            GET_SHIPPING_RATES_TOOL,
            TRACK_SHIPMENT_TOOL
        ]
        
        super().__init__(
            name="ShippingAgent",
            instructions=instructions,
            tools=tools,
            project_endpoint=project_endpoint,
            model_deployment=model_deployment
        )
    
    # def can_handle(self, query: str) -> bool:
    #     """Check if this agent can handle the query"""
    #     keywords = [
    #         "shipping", "delivery", "ship", "track", "tracking",
    #         "shipment", "arrive", "when will", "how long", "shipping rate"
    #     ]
    #     return any(keyword in query.lower() for keyword in keywords)
