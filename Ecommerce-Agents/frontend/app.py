"""
E-Commerce Multi-Agent System - Streamlit Chat Interface
=========================================================

Interactive Streamlit chat interface with intelligent agent routing.

Usage:
    streamlit run frontend/app_ecommerce.py
"""

import streamlit as st
import asyncio
import os
import sys
from pathlib import Path

# Add Agentic-System directory to path to import agents and orchestrator
agentic_system_dir = Path(__file__).resolve().parent.parent / "Agentic-System"
#print(f"🔍 Adding Agentic-System to path: {agentic_system_dir}")
if str(agentic_system_dir) not in sys.path:
    sys.path.insert(0, str(agentic_system_dir))

# Import agents and orchestrator
try:
    from agents import ProductAgent, OrderAgent, ShippingAgent, CustomerAgent
    from utils.intelligent_orchestrator import IntelligentOrchestrator
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info(f"Current working directory: {os.getcwd()}")
    st.info(f"Python path: {sys.path}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="E-Commerce AI Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .agent-info {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #2196f3;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .singleton-badge {
        background-color: #fff3cd;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_orchestrator():
    """
    Initialize orchestrator with agents ONCE using Streamlit's cache_resource.
    
    This decorator ensures:
    - Agents are created ONLY ONCE when the app starts
    - Same instance is reused across all sessions and page reruns
    - No repeated initialization overhead
    - Proper singleton pattern for production use
    """
    project_endpoint = st.secrets["azure"]["endpoint"]
    model_deployment = st.secrets["azure"]["model_deployment"]

    if not project_endpoint:
        raise ValueError("project endpoint is not set in secret file")
    
    print("🚀 [SINGLETON] Initializing agent orchestrator (runs once)...")
    
    # Initialize agents
    agents = [
        ProductAgent(project_endpoint, model_deployment),
        OrderAgent(project_endpoint, model_deployment),
        ShippingAgent(project_endpoint, model_deployment),
        CustomerAgent(project_endpoint, model_deployment)
    ]
    
    # Create orchestrator
    orchestrator = IntelligentOrchestrator(
        agents,
        endpoint=project_endpoint,
        model=model_deployment,
        use_azure_ad=True
    )
    
    # Initialize all agents
    asyncio.run(orchestrator.initialize_all_agents())
    
    print("✅ [SINGLETON] Agent orchestrator initialized successfully")
    print(f"   📊 Agents created: {len(agents)}")
    print(f"   🔗 Endpoint: {project_endpoint[:50]}...")
    print(f"   🤖 Model: {model_deployment}")
    
    return orchestrator


def initialize_session_state():
    """Initialize per-session state variables (NOT agents!)"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_routing_info" not in st.session_state:
        st.session_state.show_routing_info = True

async def get_response(query: str, orchestrator: IntelligentOrchestrator):
    """Get response from the orchestrator"""
    response = await orchestrator.route_query_with_collaboration(query) #, verbose=st.session_state.show_routing_info)
    return response


def display_sidebar():
    """Display sidebar with controls and information"""
    with st.sidebar:
        st.header("🤖 Agent System")
        
        # System status - always active with singleton pattern
        st.markdown("""
        <div class="singleton-badge">
            🟢 Agents Active (Singleton Pattern)<br>
            <small>Shared across all sessions</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        st.session_state.show_routing_info = st.checkbox(
            "Show Routing Information",
            value=True,
            help="Display which agent is handling your query"
        )
        
        st.divider()
        
        # Available Agents
        st.header("🎯 Available Agents")
        
        with st.expander("🛒 Product Agent"):
            st.markdown("""
            - Search products
            - Get product details
            - Check inventory
            - Price information
            """)
        
        with st.expander("📦 Order Agent"):
            st.markdown("""
            - Check order status
            - Create new orders
            - Cancel orders
            - Order history
            """)
        
        with st.expander("🚚 Shipping Agent"):
            st.markdown("""
            - Track shipments
            - Get shipping rates
            - Delivery estimates
            - Carrier information
            """)
        
        with st.expander("👤 Customer Agent"):
            st.markdown("""
            - Account information
            - Loyalty points
            - Redeem rewards
            - Customer profile
            """)
        
        st.divider()
        
        # Clear chat
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()        
        
def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🛍️ E-Commerce AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### Ask me anything about products, orders, shipping, or your account!")
    
    # Get orchestrator (created once, reused forever)
    try:
        orchestrator = get_orchestrator()
    except Exception as e:
        st.error(f"❌ Error initializing agents: {str(e)}")
        st.info("""
        **Setup Instructions:**
        1. Create a `secrets.toml` file inside .streamlit folder
        2. Add: `[azure] endpoint=<your-endpoint>`
        3. Add: `[azure] model_deployment=<your-model>`
        4. Run `az login` to authenticate
        """)
        st.stop()
    
    # Display sidebar
    display_sidebar()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Show agent info if available
            if "agent" in message and st.session_state.show_routing_info:
                st.markdown(f'<div class="agent-info">🤖 Handled by: {message["agent"]}</div>', 
                          unsafe_allow_html=True)
    
    # Handle example query from sidebar
    if "example_query" in st.session_state:
        query = st.session_state.example_query
        del st.session_state.example_query
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Processing your request..."):
                try:
                    response = asyncio.run(get_response(query, orchestrator))
                    st.markdown(response)
                    
                    # Extract agent info if verbose mode is on
                    agent_name = "Multi-Agent System"
                    if "ProductAgent" in response or "product" in query.lower():
                        agent_name = "Product Agent 🛒"
                    elif "OrderAgent" in response or "order" in query.lower():
                        agent_name = "Order Agent 📦"
                    elif "ShippingAgent" in response or "track" in query.lower() or "ship" in query.lower():
                        agent_name = "Shipping Agent 🚚"
                    elif "CustomerAgent" in response or "customer" in query.lower() or "loyalty" in query.lower():
                        agent_name = "Customer Agent 👤"
                    
                    if st.session_state.show_routing_info:
                        st.markdown(f'<div class="agent-info">🤖 Handled by: {agent_name}</div>', 
                                  unsafe_allow_html=True)
                    
                    # Store message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "agent": agent_name
                    })
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
        
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask about products, orders, shipping, or your account..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Processing your request..."):
                try:
                    response = asyncio.run(get_response(prompt, orchestrator))
                    st.markdown(response)
                    
                    # Extract agent info
                    agent_name = "Multi-Agent System"
                    if "ProductAgent" in response or "product" in prompt.lower():
                        agent_name = "Product Agent 🛒"
                    elif "OrderAgent" in response or "order" in prompt.lower():
                        agent_name = "Order Agent 📦"
                    elif "ShippingAgent" in response or "track" in prompt.lower() or "ship" in prompt.lower():
                        agent_name = "Shipping Agent 🚚"
                    elif "CustomerAgent" in response or "customer" in prompt.lower() or "loyalty" in prompt.lower():
                        agent_name = "Customer Agent 👤"
                    
                    if st.session_state.show_routing_info:
                        st.markdown(f'<div class="agent-info">🤖 Handled by: {agent_name}</div>', 
                                  unsafe_allow_html=True)
                    
                    # Store message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "agent": agent_name
                    })
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
        
        st.rerun()

if __name__ == "__main__":
    main()
