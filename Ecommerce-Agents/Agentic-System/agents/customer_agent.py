"""
Customer Agent - Handles customer account and loyalty programs
"""
from .base_agent import FoundryBaseAgent
from tools.function_tools import (
    GET_CUSTOMER_INFO_TOOL,
    GET_LOYALTY_POINTS_TOOL,
    REDEEM_POINTS_TOOL
)


class CustomerAgent(FoundryBaseAgent):
    """Agent specialized in customer account management"""
    
    def __init__(self, project_endpoint: str, model_deployment: str):
        instructions = """You are a Customer Account Specialist for an e-commerce platform.

Your responsibilities:
- Provide customer account information
- Help customers check their loyalty points balance
- Process loyalty points redemption for discounts
- Explain loyalty program benefits and tiers

Use the available tools to access real-time customer data from our API.
Be friendly and help customers maximize their benefits.
Clearly explain how loyalty points work (1 point = $0.01 discount)."""

        tools = [
            GET_CUSTOMER_INFO_TOOL,
            GET_LOYALTY_POINTS_TOOL,
            REDEEM_POINTS_TOOL
        ]
        
        super().__init__(
            name="CustomerAgent",
            instructions=instructions,
            tools=tools,
            project_endpoint=project_endpoint,
            model_deployment=model_deployment
        )
    
    # def can_handle(self, query: str) -> bool:
    #     """Check if this agent can handle the query"""
    #     keywords = [
    #         "account", "customer", "loyalty", "points", "rewards",
    #         "redeem", "balance", "tier", "member", "profile"
    #     ]
    #     return any(keyword in query.lower() for keyword in keywords)
