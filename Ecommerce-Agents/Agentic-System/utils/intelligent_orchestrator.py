"""
Intelligent E-Commerce Orchestrator
Uses LLM-based intent classification for smart routing to specialized agents.
"""
import asyncio
import json
import logging
from typing import List, Dict, Any

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions
from azure.identity import DefaultAzureCredential

from agents import (
    ProductAgent,
    OrderAgent,
    ShippingAgent,
    CustomerAgent
)

logger = logging.getLogger(__name__)


class IntelligentOrchestrator:
    """
    Intelligent orchestrator that uses LLM-based intent classification
    to route queries to the most appropriate agent.
    """
    
    def __init__(
        self,
        agents: List,
        endpoint: str,
        model: str,
        use_azure_ad: bool = True
    ):
        """
        Initialize intelligent orchestrator.
        
        Args:
            agents: List of specialized agents
            endpoint: Azure AI endpoint URL
            model: Model deployment name for routing
            use_azure_ad: Use Azure AD authentication (vs API key)
        """
        self.agents = agents
        self.endpoint = endpoint
        self.model = model
        self.use_azure_ad = use_azure_ad
        
        self.product_agent = None
        self.order_agent = None
        self.shipping_agent = None
        self.customer_agent = None
        
        self.routing_agent_id = None
        self.agents_client = None
        
        # Map agents by type
        for agent in agents:
            if isinstance(agent, ProductAgent):
                self.product_agent = agent
            elif isinstance(agent, OrderAgent):
                self.order_agent = agent
            elif isinstance(agent, ShippingAgent):
                self.shipping_agent = agent
            elif isinstance(agent, CustomerAgent):
                self.customer_agent = agent
    
    async def initialize_all_agents(self):
        """Initialize routing LLM agent and all agents in parallel"""
        print("\n🚀 Initializing Intelligent Multi-Agent System...")
        print("=" * 70)
        
        # Initialize routing agent using AgentsClient directly
        try:
            credential = DefaultAzureCredential()
            self.agents_client = AgentsClient(
                endpoint=self.endpoint,
                credential=credential
            )
            
            # Create routing agent for intent classification
            routing_instructions = """You are an intent classification specialist for an e-commerce multi-agent system.
Your job is to analyze user queries and classify them to the appropriate agent.

Available agents:
- ProductAgent: Handles product search, details, inventory, availability, pricing, specifications, recommendations
- OrderAgent: Handles order status, creation, placement, cancellation, history, order inquiries
- ShippingAgent: Handles shipping rates, delivery estimates, tracking, delivery status, shipping methods
- CustomerAgent: Handles account info, loyalty points, rewards, account balance, profile, customer service
- PaymentInfo: Payment queries - NOTE: All payments are offline/COD (Cash on Delivery)

Always respond with ONLY valid JSON in this format:
{
    "agent": "AgentName",
    "confidence": 0.95,
    "reasoning": "Brief explanation",
    "requires_collaboration": false,
    "secondary_agents": []
}

Rules:
- Use exact agent names from the list
- Confidence between 0.0 and 1.0
- For payment queries, use "PaymentInfo"
- If query mentions MULTIPLE topics (e.g., "product price AND order status"), set requires_collaboration=true and list ALL relevant agents in secondary_agents
- Examples of multi-intent queries:
  * "What's the price of PROD-001 and order status of ORD-12345?" → requires_collaboration=true, primary=ProductAgent, secondary_agents=["OrderAgent"]
  * "Show me laptops and when will they arrive?" → requires_collaboration=true, primary=ProductAgent, secondary_agents=["ShippingAgent"]"""
            
            routing_agent = self.agents_client.create_agent(
                model=self.model,
                name="RoutingAgent",
                instructions=routing_instructions
            )
            self.routing_agent_id = routing_agent.id
            print("✓ Routing agent initialized")
        except Exception as e:
            logger.error(f"Failed to initialize routing agent: {e}")
            raise
        
        # Initialize all agents
        init_tasks = [agent.initialize() for agent in self.agents]
        await asyncio.gather(*init_tasks)
        
        print("=" * 70)
        print("✓ All agents initialized successfully!\n")
    
    async def classify_intent(self, query: str) -> Dict[str, Any]:
        """
        Use LLM agent to classify query intent and determine routing.
        
        Args:
            query: User query
            
        Returns:
            Classification result with agent, confidence, and reasoning
        """
        try:
            # Use create_thread_and_process_run which polls until completion
            run = self.agents_client.create_thread_and_process_run(
                agent_id=self.routing_agent_id,
                thread=AgentThreadCreationOptions(
                    messages=[ThreadMessageOptions(role="user", content=f"Classify this query: \"{query}\"")]
                )
            )
            
            logger.info(f"Run status: {run.status}")
            
            if run.status == "completed":
                # List messages and find assistant response
                messages = self.agents_client.messages.list(thread_id=run.thread_id)
                
                for msg in messages:
                    if msg.role == "assistant":
                        for content_item in msg.content:
                            if hasattr(content_item, 'text'):
                                result_text = content_item.text.value.strip()
                                logger.info(f"Raw response: {result_text}")
                    
                                # Try to parse JSON
                                try:
                                    # Remove markdown code blocks if present
                                    if "```json" in result_text:
                                        result_text = result_text.split("```json")[1].split("```")[0].strip()
                                    elif "```" in result_text:
                                        result_text = result_text.split("```")[1].split("```")[0].strip()
                                    
                                    classification = json.loads(result_text)
                                    
                                    # Validate classification
                                    if "agent" not in classification:
                                        raise ValueError("Missing 'agent' field")
                                    
                                    if "confidence" not in classification:
                                        classification["confidence"] = 0.7
                                    
                                    if "reasoning" not in classification:
                                        classification["reasoning"] = "No reasoning provided"
                                    
                                    if "requires_collaboration" not in classification:
                                        classification["requires_collaboration"] = False
                                    
                                    if "secondary_agents" not in classification:
                                        classification["secondary_agents"] = []
                                    
                                    logger.info(f"Intent classification: {classification}")
                                    
                                    return classification
                                    
                                except json.JSONDecodeError as e:
                                    logger.error(f"Failed to parse JSON: {e}")
                                    logger.error(f"Response was: {result_text}")
            
            # Fallback to keyword-based routing
            logger.warning(f"LLM classification failed - run status was: {run.status}")
            return await self._fallback_classification(query)
        
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            # Fallback to keyword-based routing
            return await self._fallback_classification(query)
    
    async def _fallback_classification(self, query: str) -> Dict[str, Any]:
        """
        Fallback to simple keyword-based classification if LLM fails.
        
        Args:
            query: User query
            
        Returns:
            Classification result
        """
        query_lower = query.lower()
        
        # Payment keywords
        if any(kw in query_lower for kw in ["payment", "pay", "refund", "transaction", "charge", "credit card", "paypal", "billing"]):
            return {
                "agent": "PaymentInfo",
                "confidence": 0.8,
                "reasoning": "Fallback keyword match for payment",
                "requires_collaboration": False,
                "secondary_agents": []
            }
        
        # Order keywords
        if any(kw in query_lower for kw in ["order", "purchase", "buy", "status", "tracking", "cancel", "place order"]):
            return {
                "agent": "OrderAgent",
                "confidence": 0.7,
                "reasoning": "Fallback keyword match for orders",
                "requires_collaboration": False,
                "secondary_agents": []
            }
        
        # Shipping keywords
        if any(kw in query_lower for kw in ["shipping", "delivery", "ship", "track", "arrive", "when will"]):
            return {
                "agent": "ShippingAgent",
                "confidence": 0.7,
                "reasoning": "Fallback keyword match for shipping",
                "requires_collaboration": False,
                "secondary_agents": []
            }
        
        # Customer keywords
        if any(kw in query_lower for kw in ["account", "profile", "customer", "loyalty", "points", "reward"]):
            return {
                "agent": "CustomerAgent",
                "confidence": 0.7,
                "reasoning": "Fallback keyword match for customer service",
                "requires_collaboration": False,
                "secondary_agents": []
            }
        
        # Default to ProductAgent
        return {
            "agent": "ProductAgent",
            "confidence": 0.6,
            "reasoning": "Default fallback to product agent",
            "requires_collaboration": False,
            "secondary_agents": []
        }
    
    async def route_query(self, query: str, verbose: bool = True) -> str:
        """
        Intelligently route query to the most appropriate agent using LLM classification.
        
        Args:
            query: User query
            verbose: Whether to include routing information in response
            
        Returns:
            Agent response with optional routing metadata
        """
        # Step 1: Classify intent using LLM
        classification = await self.classify_intent(query)
        
        agent_name = classification["agent"]
        confidence = classification["confidence"]
        reasoning = classification["reasoning"]
        
        if verbose:
            print(f"\n🎯 Routing Decision:")
            print(f"   Agent: {agent_name}")
            print(f"   Confidence: {confidence:.2%}")
            print(f"   Reasoning: {reasoning}")
            if classification.get("requires_collaboration"):
                print(f"   Collaboration: Required with {classification.get('secondary_agents', [])}")
            print()
        
        # Step 2: Handle special cases
        if agent_name == "PaymentInfo":
            return "💳 [Payment Information]\nAll payments are handled offline through Cash on Delivery (COD). Your order will be placed and payment will be collected upon delivery. If you have questions about your order, I can help you check the order status."
        
        # Step 3: Route to appropriate agent
        agent = None
        emoji = "🤖"
        
        if agent_name == "ProductAgent" and self.product_agent:
            agent = self.product_agent
            emoji = "🛍️"
        elif agent_name == "OrderAgent" and self.order_agent:
            agent = self.order_agent
            emoji = "📦"
        elif agent_name == "ShippingAgent" and self.shipping_agent:
            agent = self.shipping_agent
            emoji = "🚚"
        elif agent_name == "CustomerAgent" and self.customer_agent:
            agent = self.customer_agent
            emoji = "👤"
        
        # Step 4: Execute query with selected agent
        if agent:
            try:
                response = await agent.run(query)
                
                # Add routing metadata to response if verbose
                if verbose:
                    header = f"{emoji} [{agent_name}] (Confidence: {confidence:.0%})"
                    return f"{header}\n{response}"
                else:
                    return response
            
            except Exception as e:
                logger.error(f"Error executing query with {agent_name}: {e}")
                return f"❌ Error: Failed to process query with {agent_name}. {str(e)}"
        
        # Step 5: Fallback if no agent found
        if self.product_agent:
            response = await self.product_agent.run(query)
            return f"🛍️ [Product Agent - Fallback]\n{response}"
        
        return "❌ No agent available to handle this query."
    
    async def route_query_with_collaboration(self, query: str) -> str:
        """
        Route query with potential multi-agent collaboration.
        If classification indicates collaboration is needed, queries multiple agents.
        
        Args:
            query: User query
            
        Returns:
            Combined response from multiple agents if needed
        """
        # Classify intent
        classification = await self.classify_intent(query)
        
        agent_name = classification["agent"]
        requires_collaboration = classification.get("requires_collaboration", False)
        secondary_agents = classification.get("secondary_agents", [])
        
        print(f"\n🎯 Intelligent Routing:")
        print(f"   Primary Agent: {agent_name}")
        print(f"   Confidence: {classification['confidence']:.2%}")
        
        if requires_collaboration and secondary_agents:
            print(f"   Collaboration Mode: Active")
            print(f"   Secondary Agents: {', '.join(secondary_agents)}")
        print()
        
        # Get primary agent response
        primary_response = await self.route_query(query, verbose=False)
        
        # If collaboration needed, query secondary agents
        if requires_collaboration and secondary_agents:
            responses = [f"**Primary Response ({agent_name}):**\n{primary_response}"]
            
            for secondary_name in secondary_agents:
                if secondary_name == agent_name:
                    continue  # Skip primary agent
                
                agent = None
                if secondary_name == "ProductAgent" and self.product_agent:
                    agent = self.product_agent
                elif secondary_name == "OrderAgent" and self.order_agent:
                    agent = self.order_agent
                elif secondary_name == "ShippingAgent" and self.shipping_agent:
                    agent = self.shipping_agent
                elif secondary_name == "CustomerAgent" and self.customer_agent:
                    agent = self.customer_agent
                
                if agent:
                    try:
                        secondary_response = await agent.run(query)
                        responses.append(f"\n**Additional Information ({secondary_name}):**\n{secondary_response}")
                    except Exception as e:
                        logger.error(f"Error with secondary agent {secondary_name}: {e}")
            
            return "\n".join(responses)
        
        return primary_response
    
    async def cleanup_all_agents(self):
        """Cleanup routing agent and all specialized agents"""
        print("\n🧹 Cleaning up agents...")
        
        # Delete routing agent
        if self.routing_agent_id and self.agents_client:
            try:
                self.agents_client.delete_agent(agent_id=self.routing_agent_id)
            except Exception as e:
                logger.error(f"Error deleting routing agent: {e}")
        
        # Cleanup all specialized agents
        cleanup_tasks = [agent.cleanup() for agent in self.agents]
        await asyncio.gather(*cleanup_tasks)
        
        print("✓ Cleanup completed\n")
