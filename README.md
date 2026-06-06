# Ecommerce AI Assistant
## Problem Statement
The Ecommerce AI Assistant project solves the challenge of turning natural language customer queries into accurate e-commerce actions and information retrieval.

Key problems:

- Users ask conversational questions across multiple domains like product search, order status, shipping, customer account details, and payments.
- Handling multi-intent queries robustly requires intent classification and routing, not just a single chatbot response.
- The system must interface with backend services through structured tool calls while preserving a conversational experience.
## Solution Overview
The project implements an **agentic** e-commerce assistant using:

- A Streamlit frontend for user interaction
- An intelligent orchestrator that routes queries to specialized agents
- Microsoft Foundry agents for natural language understanding and tool execution
- A FastAPI mock e-commerce backend simulating product, order, shipping, customer, and payment services<br>
#### Why this solution works<br>
  - It separates concerns: intent routing, domain-specific reasoning, tool invocation, and backend service access.
  - It enables more reliable AI behavior by using structured JSON routing and function calls.
  - It supports complex, mixed-topic queries through agent collaboration.
  - It provides a complete development-ready stack with both frontend and backend components.
## Tech Stack
- Frontend : Streamlit
- Backend : Python, FastAPI
- AI/Agent : Microsoft Foundry Agent Service
- LLM : GPT 4.1
- Cloud : Azure
- Deployment : Azure App Service
## Key Features
- **Multi-Agent Orchestration**
  
  - Uses an IntelligentOrchestrator to route queries to the right expert agent.
    
- **LLM-Based Intent Routing**

  - A dedicated routing agent classifies user intent and chooses the appropriate domain.
    
- **Domain-Specific Agents**

  - Separate agents for Product, Order, Shipping, and Customer workflows.
    
- **Function Tool Integration**

  - Agents invoke structured tool calls instead of relying on freeform model output.
    
- **Async Execution**

  - Uses asyncio for concurrent agent initialization and query handling.
    
- **Fallback Routing**

  - Keyword-based fallback keeps the system robust when LLM routing fails.
    
- **Modular Architecture**

  - Clear separation between UI, orchestrator, agents, tool definitions, and backend API.
 
## Application Architecture
<img width="1536" height="1024" alt="ecommerce-architecture" src="https://github.com/user-attachments/assets/a75eedb9-c504-440d-8a12-4ac5a3e47951" />

