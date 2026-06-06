# Project-ECommerce Architecture Diagram

## Overview
This architecture describes the E-Commerce multi-agent system and the mock API backend.
It includes the Streamlit frontend, the Azure AI Foundry-powered agents, the intelligent orchestrator, and the FastAPI mock API.

## Diagram

```mermaid
flowchart LR
    subgraph Frontend[Frontend]
        Browser[User Browser / Streamlit UI]
        Streamlit[Streamlit App\nEcommerce-Agents/frontend/app_ecommerce.py]
    end

    subgraph Agentic_System[Agentic-System]
        Orchestrator[Intelligent Orchestrator\nEcommerce-Agents/Agentic-System/utils/intelligent_orchestrator.py]
        RoutingAgent[Routing Agent (LLM)\nIntent classification]
        ProductAgent[Product Agent\nProductAgent]
        OrderAgent[Order Agent\nOrderAgent]
        ShippingAgent[Shipping Agent\nShippingAgent]
        CustomerAgent[Customer Agent\nCustomerAgent]
        BaseAgent[FoundryBaseAgent\nbase_agent.py]
        ToolDefinitions[Function Tools\ntools/function_tools.py]
        APIClient[API Client\napi/api_client_simple.py]
        AzureFoundry[Azure AI Foundry / Agents Client]
    end

    subgraph Ecommerce_API[Ecommerce-API (FastAPI)]
        APIServer[FastAPI App\nEcommerce-API/main.py]
        ProductRoute[Product Routes]
        OrderRoute[Order Routes]
        ShippingRoute[Shipping Routes]
        CustomerRoute[Customer Routes]
        PaymentRoute[Payment Routes]
        MockData[Mock Data Layer\nEcommerce-API/data/mock_ecommerce_data.py]
    end

    Browser -->|User enters query| Streamlit
    Streamlit -->|Calls orchestrator| Orchestrator
    Orchestrator -->|Routes intent| RoutingAgent
    RoutingAgent -->|Returns JSON routing| Orchestrator

    Orchestrator -->|Delegates query| ProductAgent
    Orchestrator -->|Delegates query| OrderAgent
    Orchestrator -->|Delegates query| ShippingAgent
    Orchestrator -->|Delegates query| CustomerAgent

    ProductAgent -->|Uses Azure AI Agents| AzureFoundry
    OrderAgent -->|Uses Azure AI Agents| AzureFoundry
    ShippingAgent -->|Uses Azure AI Agents| AzureFoundry
    CustomerAgent -->|Uses Azure AI Agents| AzureFoundry

    ProductAgent -->|Calls tool functions| ToolDefinitions
    OrderAgent -->|Calls tool functions| ToolDefinitions
    ShippingAgent -->|Calls tool functions| ToolDefinitions
    CustomerAgent -->|Calls tool functions| ToolDefinitions

    ToolDefinitions -->|HTTP calls| APIClient
    APIClient -->|REST calls| APIServer

    APIServer --> ProductRoute
    APIServer --> OrderRoute
    APIServer --> ShippingRoute
    APIServer --> CustomerRoute
    APIServer --> PaymentRoute
    APIServer -.->|Reads mock data| MockData
```


## Component Responsibilities

- **Streamlit App** (`frontend/app_ecommerce.py`)
  - Presents chat UI for user queries.
  - Initializes the orchestrator and displays agent responses.

- **Intelligent Orchestrator** (`Agentic-System/utils/intelligent_orchestrator.py`)
  - Creates a routing agent for intent classification.
  - Initializes specialized agents in parallel.
  - Routes each user query to the best agent or multiple agents when collaboration is needed.

- **Specialized Agents**
  - `ProductAgent`: product search, details, inventory.
  - `OrderAgent`: order status, create, cancel.
  - `ShippingAgent`: shipping rates, tracking, delivery.
  - `CustomerAgent`: account info, loyalty points, redemption.

- **Tool Definitions** (`Agentic-System/tools/function_tools.py`)
  - Define function call interfaces for agent tools.
  - Map structured tool requests to backend API calls.

- **API Client** (`Agentic-System/api/api_client_simple.py`)
  - Sends HTTP requests to the mock e-commerce backend.
  - Handles product, inventory, order, shipping, payment, and customer endpoints.

- **Mock E-Commerce API** (`Ecommerce-API/main.py`)
  - Hosts REST endpoints via FastAPI.
  - Exposes product, order, shipping, customer, and payment routes.

## Deployment Notes

- The agent layer relies on Azure AI Foundry for LLM-based routing and tool execution.
- The frontend uses Streamlit and caches the orchestrator for better performance.
- The API backend is a mock server meant for development and demonstration.
