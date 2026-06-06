"""
Base Agent Class for E-Commerce Multi-Agent System
"""
from typing import List, Dict
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import AgentThreadCreationOptions, ThreadMessageOptions, ToolSet, FunctionTool
from azure.identity import DefaultAzureCredential
from tools.function_tools import get_callable_functions


class FoundryBaseAgent:
    """Base class for all Foundry agents"""
    
    def __init__(self, name: str, instructions: str, tools: List[Dict], project_endpoint: str, model_deployment: str):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.project_endpoint = project_endpoint
        self.model_deployment = model_deployment
        self.agent_id = None
        self.agents_client = None
        self.toolset = None
        
    async def initialize(self):
        """Initialize the agent with Azure AI Foundry"""
        try:
            credential = DefaultAzureCredential()
            self.agents_client = AgentsClient(
                endpoint=self.project_endpoint,
                credential=credential
            )
            
            # Get callable functions for this agent's tools
            tool_names = [t["function"]["name"] for t in self.tools if t.get("type") == "function"]
            callable_funcs = get_callable_functions(tool_names)
            
            # Create toolset with FunctionTool and enable auto function calls
            if callable_funcs:
                self.toolset = ToolSet()
                self.toolset.add(FunctionTool(callable_funcs))
                # Enable automatic function execution
                self.agents_client.enable_auto_function_calls(self.toolset)
            
            # Create agent with tool definitions from toolset
            agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name=self.name,
                instructions=self.instructions,
                tools=self.toolset.definitions if self.toolset else None
            )
            self.agent_id = agent.id
            print(f"✓ Agent '{self.name}' initialized (ID: {self.agent_id})")
            
        except Exception as e:
            raise Exception(f"Failed to initialize agent '{self.name}': {str(e)}")
    
    async def run(self, message: str) -> str:
        """Run the agent with a message"""
        if not self.agent_id:
            await self.initialize()
        
        try:
            # Use create_thread_and_process_run which handles polling and tool execution
            run = self.agents_client.create_thread_and_process_run(
                agent_id=self.agent_id,
                thread=AgentThreadCreationOptions(
                    messages=[ThreadMessageOptions(role="user", content=message)]
                ),
                toolset=self.toolset
            )
            
            # Get response from completed run using messages operations
            if run.status == "completed":
                # List messages and find assistant response
                messages = self.agents_client.messages.list(thread_id=run.thread_id)
                for msg in messages:
                    if msg.role == "assistant":
                        for content_item in msg.content:
                            if hasattr(content_item, 'text'):
                                return content_item.text.value
            
            return f"Agent completed with status: {run.status}"
            
        except Exception as e:
            return f"Error in agent '{self.name}': {str(e)}"
    
    async def cleanup(self):
        """Delete the agent"""
        if self.agent_id and self.agents_client:
            try:
                self.agents_client.delete_agent(agent_id=self.agent_id)
                print(f"✓ Agent '{self.name}' deleted")
            except Exception as e:
                print(f"✗ Failed to delete agent '{self.name}': {e}")
