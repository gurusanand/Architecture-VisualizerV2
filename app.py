"""
Enterprise Agent Platform - Architecture Visualizer
Interactive Streamlit application for visualizing the architecture and request flow
"""

import streamlit as st
import json
import graphviz
from auth import check_authentication, show_logout_button
from architecture_data import COMPONENTS, LAYERS, FLOWS, SAMPLE_QUERIES, RAG_FLOW, MCP_FLOW
from drawio_exporter import export_to_drawio
from planner_functions import show_planner_details, show_decision_flow_tables
from numbered_flow_diagram import create_numbered_flow_diagram, create_numbered_flow_diagram_vertical, get_flow_summary
from openapi_flow_definitions import OPENAPI_MCP_FLOW, FLOW_COMPARISON, get_flow_comparison_summary
from architecture_comparison import show_architecture_comparison
from airport_transfer_page import show_airport_transfer_use_case
from prompt_display import show_openapi_prompts
from hld_page import show_high_level_architecture

# Load enhanced component details
try:
    with open('enhanced_component_details.json', 'r') as f:
        ENHANCED_DETAILS = json.load(f)
except:
    ENHANCED_DETAILS = {}
import time

# Page configuration
st.set_page_config(
    page_title="Enterprise Agent Platform - Architecture Visualizer",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2563EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .component-box {
        border: 2px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #EFF6FF;
    }
    .component-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1E40AF;
        margin-bottom: 5px;
    }
    .technical-text {
        color: #374151;
        font-size: 0.95rem;
        margin: 5px 0;
        padding: 10px;
        background-color: #F3F4F6;
        border-left: 3px solid #3B82F6;
    }
    .layman-text {
        color: #059669;
        font-size: 0.95rem;
        margin: 5px 0;
        padding: 10px;
        background-color: #ECFDF5;
        border-left: 3px solid #10B981;
    }
    .flow-step {
        background-color: #DBEAFE;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 4px solid #3B82F6;
    }
    .layer-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: bold;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication first
if not check_authentication():
    st.stop()

# Title
st.markdown('<div class="main-header">🏗️ Enterprise Agent Platform - Architecture Visualizer</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1E3A8A/FFFFFF?text=Enterprise+Agent+Platform")
    
    st.markdown("### 📋 Navigation")
    view_mode = st.radio(
        "Select a page:",
        ["🏠 Overview", "📐 High Level Architecture", "🔍 Component Explorer", "🧠 Planner Agent Details", "🚀 Request Flow Simulator", "🎯 Numbered Flows", "📊 Full Architecture", "📝 Decision Flow Tables", "🤖 OpenAPI Prompts", "✈️ Use Case: Airport Transfer"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This visualizer helps you understand how the Enterprise Agent Platform processes requests from start to finish.
    
    **Features:**
    - Interactive architecture diagram
    - Component-by-component explanations
    - Request flow simulation
    - Technical & layman explanations
    """)
    
    st.markdown("---")
    st.markdown("### 🎨 Legend")
    st.markdown("🔵 **Technical**: For developers and architects")
    st.markdown("🟢 **Layman**: For business users and stakeholders")
    
    # OpenAPI Key Configuration
    st.markdown("---")
    st.markdown("### 🔑 OpenAPI Configuration")
    
    if 'openapi_key' not in st.session_state:
        st.session_state.openapi_key = ""
    
    with st.expander("Configure OpenAPI Key", expanded=False):
        api_key = st.text_input(
            "OpenAPI Key",
            value=st.session_state.openapi_key,
            type="password",
            help="Enter your OpenAPI key for LLM integration"
        )
        
        if st.button("Save API Key", use_container_width=True):
            st.session_state.openapi_key = api_key
            st.success("✅ API Key saved!")
        
        if st.session_state.openapi_key:
            st.info(f"🔐 API Key configured ({len(st.session_state.openapi_key)} characters)")
        else:
            st.warning("⚠️ No API Key configured")
    
    # Show logout button
    show_logout_button()


def show_overview():
    """Display the overview page"""
    st.markdown('<div class="sub-header">📖 Platform Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What is this platform?
        
        The **Enterprise Agent Platform** is a sophisticated AI-powered system that handles customer requests 
        using multiple specialized agents working together. Think of it as a smart customer service center 
        where different experts collaborate to solve your problems.
        
        ### Key Capabilities
        
        - 🤖 **AI-Powered Responses**: Uses advanced language models to understand and respond
        - 🔐 **Enterprise Security**: Bank-grade security with multiple protection layers
        - 🧠 **Memory & Personalization**: Remembers your preferences and history
        - ⚡ **High Performance**: Handles thousands of requests simultaneously
        - 📊 **Full Auditability**: Every action is logged for compliance
        """)
    
    with col2:
        st.markdown("""
        ### How does it work?
        
        1. **You send a request** (via chat, voice, or app)
        2. **Security checks** verify your identity and protect against threats
        3. **AI Planner** analyzes your request and creates a plan
        4. **Specialized Agents** work on your specific needs
        5. **Quality Checker** validates the response
        6. **You receive** an accurate, personalized answer
        
        ### Architecture Layers
        """)
        
        # Display layers
        for layer_id, layer_info in sorted(LAYERS.items(), key=lambda x: x[1]['order']):
            st.markdown(f"""
            <div style="background-color: {layer_info['color']}; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #3B82F6;">
                <strong>{layer_info['order']}. {layer_info['name']}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Protocol information
    with st.expander("📡 Message Exchange Protocols", expanded=False):
        st.markdown("""
        ### Communication Protocols Used
        
        **HTTPS/REST**
        - Customer → API Gateway
        - API Gateway → Internal Services
        - Services → External APIs
        
        **gRPC**
        - Executor → Domain Agents (high performance)
        - Agent-to-Agent communication
        - Observability telemetry
        
        **Redis Pub/Sub**
        - Agent coordination in multi-agent scenarios
        - Circuit breaker events
        - Cache invalidation
        
        **Kafka Protocol**
        - Agents → Kafka (execution events)
        - Governance → Kafka (compliance alerts)
        - Kafka Connect → Kafka (CDC events)
        - Kafka → Analytics/Audit Services
        
        **Database Protocols**
        - MongoDB: Wire Protocol
        - Redis: RESP3
        - Cosmos DB: HTTPS
        - PostgreSQL: Native protocol
        """)
    
    with st.expander("🤝 Agent-to-Agent Communication", expanded=False):
        st.markdown("""
        ### Multi-Agent Coordination
        
        **Scenario 1: Parallel Execution**
        - Executor broadcasts to multiple agents via gRPC
        - Agents process independently
        - Results aggregated by Executor
        
        **Scenario 2: Agent Collaboration**
        - Card Agent needs loan information
        - Publishes request to Redis Pub/Sub channel: `agent-coordination`
        - Loan Agent subscribes and responds
        - Enables cross-domain intelligence
        
        **Scenario 3: Sequential Handoff**
        - Card Agent completes initial processing
        - Hands off to Loan Agent for cross-sell
        - State passed via shared memory (Redis)
        """)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown('<div class="sub-header">📊 Platform Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Components", len(COMPONENTS))
    with col2:
        st.metric("Integration Points", len([f for f in FLOWS if 'external' in [COMPONENTS[f['from']]['layer'], COMPONENTS[f['to']]['layer']]]))
    with col3:
        st.metric("Security Layers", len([c for c in COMPONENTS.values() if c['layer'] == 'security']))
    with col4:
        st.metric("Specialized Agents", len([c for c in COMPONENTS.values() if c['layer'] == 'agents']))
    
    st.markdown("---")
    st.markdown('<div class="sub-header">📦 Deployment Architecture</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        container_count = sum(1 for c in ENHANCED_DETAILS.values() if c.get('deployment_type', '').startswith('Container'))
        st.metric("⭐ Containerized Services", container_count)
        st.caption("Kubernetes microservices")
    
    with col2:
        managed_count = sum(1 for c in ENHANCED_DETAILS.values() if 'Managed' in c.get('deployment_type', ''))
        st.metric("☁️ Managed Services", managed_count)
        st.caption("Azure PaaS services")
    
    with col3:
        external_count = sum(1 for c in ENHANCED_DETAILS.values() if c.get('deployment_type', '').startswith('External'))
        st.metric("🌐 External APIs", external_count)
        st.caption("Backend systems")
    
    # Kafka visibility callout
    st.info("""
    📨 **Kafka & Event Streaming**: The platform includes 5 Kafka-related components for async event streaming:
    - **Kafka Broker** (📨) - 10K+ msgs/sec, 6 topics
    - **Zookeeper** (🎯) - Kafka coordination
    - **Kafka Connect** (🔄) - Database CDC
    - **Analytics Service** (📊) - Real-time metrics
    - **Audit Service** (📝) - Compliance logging
    
    **To view Kafka components:**
    - Go to **Full Architecture** → Enable **"Messaging & Streaming"** layer filter
    - Or go to **Component Explorer** → Filter by **"Messaging & Streaming"**
    """)


def show_component_explorer():
    """Display detailed component information"""
    st.markdown('<div class="sub-header">🔍 Component Explorer</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Explore each component in detail. Components marked with ⭐ are containerized microservices running in Kubernetes.
    See database operations, API calls, deployment architecture, and message protocols for each component.
    """)
    
    st.info("💡 **Tip:** Look for the 'Deployment Architecture' section in each component to see if it's a container (⭐ Microservice), managed service (☁️ Azure PaaS), or external API (🌐 Backend).")
    
    # Layer filter
    col1, col2 = st.columns([1, 2])
    
    with col1:
        deployment_filter = st.selectbox(
            "Filter by Deployment:",
            ["All Types", "⭐ Containers Only", "☁️ Managed Services", "🌐 External APIs"]
        )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_layer = st.selectbox(
            "Filter by Layer:",
            ["All Layers"] + [layer_info['name'] for layer_info in sorted(LAYERS.values(), key=lambda x: x['order'])]
        )
    
    with col2:
        search_term = st.text_input("🔎 Search components:", placeholder="Type component name...")
    
    # Filter components
    filtered_components = {}
    for comp_id, comp_data in COMPONENTS.items():
        # Apply layer filter
        if selected_layer != "All Layers":
            layer_name = LAYERS[comp_data['layer']]['name']
            if layer_name != selected_layer:
                continue
        
        # Apply deployment filter
        if deployment_filter != "All Types":
            if comp_id in ENHANCED_DETAILS:
                deployment_type = ENHANCED_DETAILS[comp_id].get('deployment_type', '')
                if deployment_filter == "⭐ Containers Only" and 'Container' not in deployment_type:
                    continue
                elif deployment_filter == "☁️ Managed Services" and 'Managed' not in deployment_type:
                    continue
                elif deployment_filter == "🌐 External APIs" and not deployment_type.startswith('External'):
                    continue
            else:
                # Skip if no deployment info and filter is active
                continue
        
        # Apply search filter
        if search_term and search_term.lower() not in comp_data['name'].lower():
            continue
        
        filtered_components[comp_id] = comp_data
    
    # Display components
    st.markdown(f"**Showing {len(filtered_components)} component(s)**")
    
    for comp_id, comp_data in filtered_components.items():
        layer_info = LAYERS[comp_data['layer']]
        
        # Add deployment indicator
        deployment_indicator = ""
        if comp_id in ENHANCED_DETAILS:
            deployment_type = ENHANCED_DETAILS[comp_id].get('deployment_type', '')
            if 'Container' in deployment_type:
                deployment_indicator = " ⭐"
            elif 'Managed' in deployment_type:
                deployment_indicator = " ☁️"
            elif deployment_type.startswith('External'):
                deployment_indicator = " 🌐"
        
        with st.expander(f"{comp_data['icon']} {comp_data['name']}{deployment_indicator} - {layer_info['name']}", expanded=False):
            st.markdown(f"""
            <div class="component-box">
                <div class="component-title">{comp_data['icon']} {comp_data['name']}</div>
                
                <div style="margin: 10px 0;">
                    <span class="layer-badge" style="background-color: {layer_info['color']}; color: #1E3A8A;">
                        {layer_info['name']}
                    </span>
                </div>
                
                <div style="margin-top: 15px;">
                    <strong>🔵 Technical Explanation:</strong>
                    <div class="technical-text">
                        {comp_data['technical']}
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <strong>🟢 Layman Explanation:</strong>
                    <div class="layman-text">
                        {comp_data['layman']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show enhanced details if available
            if comp_id in ENHANCED_DETAILS:
                details = ENHANCED_DETAILS[comp_id]
                
                st.markdown("---")
                st.markdown("### 💾 Database Operations")
                
                if details.get('databases'):
                    st.markdown(f"**Databases Used:** {', '.join(details['databases'])}")
                
                if details.get('mongodb_ops'):
                    st.markdown("**MongoDB Operations:**")
                    for op in details['mongodb_ops']:
                        st.code(op, language="javascript")
                
                if details.get('redis_ops'):
                    st.markdown("**Redis Operations:**")
                    for op in details['redis_ops']:
                        st.code(op, language="redis")
                
                if details.get('cosmos_ops'):
                    st.markdown("**Cosmos DB Operations:**")
                    for op in details['cosmos_ops']:
                        st.code(op, language="sql")
                
                if details.get('functions'):
                    st.markdown("### ⚙️ Key Functions")
                    for func in details['functions']:
                        st.markdown(f"- `{func}`")
                
                if details.get('api_calls'):
                    st.markdown("### 🌐 External API Calls")
                    for api in details['api_calls']:
                        st.code(api, language="http")
                
                # Show deployment information
                if details.get('deployment_type'):
                    st.markdown("### 📦 Deployment Architecture")
                    
                    deployment_type = details['deployment_type']
                    is_container = 'Container' in deployment_type
                    
                    if is_container:
                        st.markdown(f"**Type:** {deployment_type} ⭐ *Microservice*")
                    else:
                        st.markdown(f"**Type:** {deployment_type}")
                    
                    if details.get('replicas') and details['replicas'] != 'N/A':
                        st.markdown(f"**Replicas:** {details['replicas']}")
                    
                    if details.get('container_image'):
                        st.markdown(f"**Container Image:** `{details['container_image']}`")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if details.get('inbound_protocol'):
                            st.markdown(f"🔽 **Inbound:** {details['inbound_protocol']}")
                    with col2:
                        if details.get('outbound_protocol'):
                            st.markdown(f"🔼 **Outbound:** {details['outbound_protocol']}")
                    
                    if details.get('agent_coordination'):
                        st.info(f"🤝 **Agent Coordination:** {details['agent_coordination']}")
                    
                    if details.get('authentication'):
                        st.markdown(f"🔐 **Authentication:** {details['authentication']}")
                    
                    if details.get('endpoints'):
                        st.markdown("**API Endpoints:**")
                        for endpoint in details['endpoints']:
                            st.code(endpoint, language="http")
            
            # Show connections with protocols
            incoming = [f for f in FLOWS if f['to'] == comp_id]
            outgoing = [f for f in FLOWS if f['from'] == comp_id]
            
            if incoming or outgoing:
                st.markdown("**🔗 Connections & Data Flow:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if incoming:
                        st.markdown("**⬅️ Incoming:**")
                        for flow in incoming:
                            from_comp = COMPONENTS[flow['from']]
                            st.markdown(f"- {from_comp['icon']} {from_comp['name']} → *{flow['label']}*")
                
                with col2:
                    if outgoing:
                        st.markdown("**➡️ Outgoing:**")
                        for flow in outgoing:
                            to_comp = COMPONENTS[flow['to']]
                            st.markdown(f"- *{flow['label']}* → {to_comp['icon']} {to_comp['name']}")


def show_request_simulator():
    """Display interactive request flow simulator"""
    st.markdown('<div class="sub-header">🚀 Request Flow Simulator</div>', unsafe_allow_html=True)
    
    st.markdown("""
    See how different types of requests flow through the system. Select a sample query or enter your own
    to visualize the complete journey from input to output.
    """)
    
    # Query input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query_type = st.selectbox(
            "Select a sample query:",
            ["Custom Query"] + list(SAMPLE_QUERIES.keys())
        )
    
    with col2:
        show_animation = st.checkbox("Animate Flow", value=True)
    
    if query_type == "Custom Query":
        user_query = st.text_area(
            "Enter your query:",
            placeholder="E.g., I want to check my account balance and apply for a credit card",
            height=100
        )
        
        if user_query:
            # Simple intent classification
            intent = classify_intent(user_query)
            st.info(f"🎯 Detected Intent: **{intent}**")
            
            # Get path based on intent
            if intent in ["card", "loan", "wealth"]:
                path = get_path_for_intent(intent)
            else:
                path = SAMPLE_QUERIES["General Question"]["path"]
            
            explanation = f"Based on your query, the system will route this through the {intent} processing pipeline."
        else:
            st.warning("Please enter a query to simulate the flow.")
            return
    else:
        query_data = SAMPLE_QUERIES[query_type]
        user_query = query_data["query"]
        intent = query_data["intent"]
        path = query_data["path"]
        explanation = query_data["explanation"]
        
        st.text_area("Query:", value=user_query, height=100, disabled=True)
        st.info(f"🎯 Intent: **{intent.title()}**")
    
    # Display explanation
    st.markdown("### 📝 Flow Explanation")
    st.markdown(f"""
    <div style="background-color: #F0F9FF; padding: 15px; border-radius: 10px; border-left: 4px solid #3B82F6;">
        {explanation}
    </div>
    """, unsafe_allow_html=True)
    
    # Determine request/response split point
    # Find where the flow reaches the furthest point (usually an external API or database)
    # Then everything after is the response path
    split_point = len(path) // 2  # Simple heuristic: halfway point
    
    # Better heuristic: find the last external/data component
    for i in range(len(path) - 1, -1, -1):
        if path[i] in ['accounts_api', 'cards_api', 'loans_api', 'crm', 'cosmos_db', 'vector_db']:
            split_point = i + 1
            break
    
    request_path = path[:split_point]
    response_path = path[split_point:]
    
    # Visualize flow with bidirectional separation
    st.markdown("### 🔄 Complete Bidirectional Flow")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ➡️ Request Path (Forward)")
        st.caption(f"{len(request_path)} steps")
    with col2:
        st.markdown("#### ⬅️ Response Path (Backward)")
        st.caption(f"{len(response_path)} steps")
    
    if show_animation:
        # Animated flow
        progress_bar = st.progress(0)
        status_text = st.empty()
        flow_container = st.container()
        
        # Request path
        status_text.markdown("🚀 **Request Phase: Forwarding to backend...**")
        for i, comp_id in enumerate(request_path):
            comp_data = COMPONENTS[comp_id]
            layer_info = LAYERS[comp_data['layer']]
            
            # Get deployment indicator
            deployment_badge = ""
            protocol_info = ""
            if comp_id in ENHANCED_DETAILS:
                details = ENHANCED_DETAILS[comp_id]
                deployment_type = details.get('deployment_type', '')
                if 'Container' in deployment_type:
                    deployment_badge = " ⭐"
                elif 'Managed' in deployment_type:
                    deployment_badge = " ☁️"
                elif deployment_type.startswith('External'):
                    deployment_badge = " 🌐"
                
                # Get protocol for next step
                if i < len(request_path) - 1:
                    outbound = details.get('outbound_protocol', '')
                    if outbound:
                        protocol_info = f"<br/><small style='color: #8B5CF6;'>📡 {outbound}</small>"
            
            progress = (i + 1) / len(path)
            progress_bar.progress(progress)
            status_text.markdown(f"**Step {i+1}/{len(path)}:** ➡️ Processing at {comp_data['name']}...")
            
            with flow_container:
                st.markdown(f"""
                <div class="flow-step" style="animation: fadeIn 0.5s; border-left: 4px solid #3B82F6;">
                    <strong>{i+1}. {comp_data['icon']} {comp_data['name']}{deployment_badge}</strong>
                    <br/>
                    <small style="color: #6B7280;">{layer_info['name']}</small>
                    <br/>
                    <span style="color: #059669; font-size: 0.9rem;">{comp_data['layman']}</span>
                    {protocol_info}
                </div>
                """, unsafe_allow_html=True)
            
            time.sleep(0.3)  # Animation delay
        
        # Response path
        status_text.markdown("🔙 **Response Phase: Returning to customer...**")
        for i, comp_id in enumerate(response_path):
            comp_data = COMPONENTS[comp_id]
            layer_info = LAYERS[comp_data['layer']]
            
            # Get deployment indicator
            deployment_badge = ""
            protocol_info = ""
            if comp_id in ENHANCED_DETAILS:
                details = ENHANCED_DETAILS[comp_id]
                deployment_type = details.get('deployment_type', '')
                if 'Container' in deployment_type:
                    deployment_badge = " ⭐"
                elif 'Managed' in deployment_type:
                    deployment_badge = " ☁️"
                elif deployment_type.startswith('External'):
                    deployment_badge = " 🌐"
                
                # Get protocol for next step
                if i < len(response_path) - 1:
                    inbound = details.get('inbound_protocol', '')
                    if inbound:
                        protocol_info = f"<br/><small style='color: #8B5CF6;'>📡 {inbound}</small>"
            
            actual_step = len(request_path) + i + 1
            progress = actual_step / len(path)
            progress_bar.progress(progress)
            status_text.markdown(f"**Step {actual_step}/{len(path)}:** ⬅️ Returning through {comp_data['name']}...")
            
            with flow_container:
                st.markdown(f"""
                <div class="flow-step" style="animation: fadeIn 0.5s; border-left: 4px solid #10B981;">
                    <strong>{actual_step}. {comp_data['icon']} {comp_data['name']}{deployment_badge}</strong>
                    <br/>
                    <small style="color: #6B7280;">{layer_info['name']}</small>
                    <br/>
                    <span style="color: #059669; font-size: 0.9rem;">{comp_data['layman']}</span>
                    {protocol_info}
                </div>
                """, unsafe_allow_html=True)
            
            time.sleep(0.3)  # Animation delay
        
        status_text.markdown("✅ **Request completed successfully! Response delivered to customer.**")
    else:
        # Static flow with bidirectional display
        st.markdown("#### ➡️ Request Path")
        for i, comp_id in enumerate(request_path):
            comp_data = COMPONENTS[comp_id]
            layer_info = LAYERS[comp_data['layer']]
            
            # Get deployment indicator and protocol
            deployment_badge = ""
            protocol_info = ""
            if comp_id in ENHANCED_DETAILS:
                details = ENHANCED_DETAILS[comp_id]
                deployment_type = details.get('deployment_type', '')
                if 'Container' in deployment_type:
                    deployment_badge = " ⭐"
                elif 'Managed' in deployment_type:
                    deployment_badge = " ☁️"
                elif deployment_type.startswith('External'):
                    deployment_badge = " 🌐"
                
                if i < len(request_path) - 1:
                    outbound = details.get('outbound_protocol', '')
                    if outbound:
                        protocol_info = f"<br/><small style='color: #8B5CF6;'>📡 {outbound}</small>"
            
            st.markdown(f"""
            <div class="flow-step" style="border-left: 4px solid #3B82F6;">
                <strong>{i+1}. {comp_data['icon']} {comp_data['name']}{deployment_badge}</strong>
                <br/>
                <small style="color: #6B7280;">{layer_info['name']}</small>
                <br/>
                <span style="color: #059669; font-size: 0.9rem;">{comp_data['layman']}</span>
                {protocol_info}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### ⬅️ Response Path")
        for i, comp_id in enumerate(response_path):
            comp_data = COMPONENTS[comp_id]
            layer_info = LAYERS[comp_data['layer']]
            
            # Get deployment indicator and protocol
            deployment_badge = ""
            protocol_info = ""
            if comp_id in ENHANCED_DETAILS:
                details = ENHANCED_DETAILS[comp_id]
                deployment_type = details.get('deployment_type', '')
                if 'Container' in deployment_type:
                    deployment_badge = " ⭐"
                elif 'Managed' in deployment_type:
                    deployment_badge = " ☁️"
                elif deployment_type.startswith('External'):
                    deployment_badge = " 🌐"
                
                if i < len(response_path) - 1:
                    inbound = details.get('inbound_protocol', '')
                    if inbound:
                        protocol_info = f"<br/><small style='color: #8B5CF6;'>📡 {inbound}</small>"
            
            actual_step = len(request_path) + i + 1
            st.markdown(f"""
            <div class="flow-step" style="border-left: 4px solid #10B981;">
                <strong>{actual_step}. {comp_data['icon']} {comp_data['name']}{deployment_badge}</strong>
                <br/>
                <small style="color: #6B7280;">{layer_info['name']}</small>
                <br/>
                <span style="color: #059669; font-size: 0.9rem;">{comp_data['layman']}</span>
                {protocol_info}
            </div>
            """, unsafe_allow_html=True)
    
    # Generate flow diagram
    st.markdown("### 📊 Flow Diagram")
    flow_graph = create_flow_diagram(path)
    st.graphviz_chart(flow_graph)


def show_numbered_flows():
    """Display numbered flow diagrams with color coding"""
    st.markdown('<div class="sub-header">🎯 Numbered Flow Sequences</div>', unsafe_allow_html=True)
    
    # Architecture toggle switch
    st.markdown("### 🔄 Architecture Type")
    architecture_type = st.radio(
        "Select architecture implementation:",
        ["Code-Based (Current Implementation)", "OpenAPI-Based (Alternative Architecture)", "Comparison (Both)"],
        horizontal=True
    )
    
    # Show description based on selection
    if architecture_type == "Code-Based (Current Implementation)":
        st.info("""
        🔵 **Code-Based Architecture**: Current implementation using hardcoded MCP tool schemas and direct function calls.
        - **Pros**: Fast, type-safe, simple
        - **Cons**: Requires code changes for new APIs
        - **Color**: Blue (#0066CC)
        """)
    elif architecture_type == "OpenAPI-Based (Alternative Architecture)":
        st.info("""
        🟪 **OpenAPI-Based Architecture**: Alternative using OpenAPI specs for dynamic tool discovery.
        - **Pros**: Dynamic, loose coupling, self-documenting
        - **Cons**: Slower, more complex
        - **Color**: Purple (#7C3AED)
        """)
    else:
        st.info("""
        🔄 **Comparison Mode**: View both architectures side-by-side to understand trade-offs.
        - Blue: Code-Based (21 steps, 512ms)
        - Purple: OpenAPI-Based (27 steps, 612ms)
        """)
    
    st.markdown("---")
    
    # Conditional content based on architecture type
    if architecture_type == "Comparison (Both)":
        show_architecture_comparison()
        return
    
    # Determine which flow to show
    is_openapi = architecture_type == "OpenAPI-Based (Alternative Architecture)"
    
    st.markdown("""
    This page shows two different data retrieval patterns with numbered sequences:
    - **🟢 Dark Green**: RAG Knowledge Retrieval (11 steps)
    - **🔵 Blue** (Code-Based) / **🟪 Purple** (OpenAPI-Based): MCP Tool Call to Accounts API
    """)
    
    # Flow selection
    col1, col2 = st.columns([1, 2])
    with col1:
        flow_type = st.selectbox(
            "Select Flow to Display:",
            ["Both Flows", "RAG Flow Only", "MCP Flow Only"]
        )
    
    with col2:
        diagram_orientation = st.selectbox(
            "Diagram Orientation:",
            ["Horizontal (Left to Right)", "Vertical (Top to Bottom)"]
        )
    
    # Map selection to flow type parameter
    flow_param = "both"
    if flow_type == "RAG Flow Only":
        flow_param = "rag"
    elif flow_type == "MCP Flow Only":
        flow_param = "mcp_openapi" if is_openapi else "mcp"
    
    # Display flow summaries
    st.markdown("### 📊 Flow Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟢 RAG Knowledge Retrieval")
        rag_summary = get_flow_summary("rag")
        st.markdown(f"""
        - **Steps**: {rag_summary['steps']}
        - **Latency**: {rag_summary['latency']}
        - **Data Source**: {rag_summary['data_source']}
        - **Agent Involved**: {rag_summary['agent_involved']}
        - **LLM Call**: {rag_summary['llm_call']}
        - **External API**: {rag_summary['external_api']}
        - **Governance**: {rag_summary['governance']}
        
        **Use Cases**: {', '.join(rag_summary['use_cases'])}
        """)
    
    with col2:
        st.markdown("#### 🔵 MCP Tool Call to Accounts API")
        mcp_summary = get_flow_summary("mcp")
        st.markdown(f"""
        - **Steps**: {mcp_summary['steps']}
        - **Latency**: {mcp_summary['latency']}
        - **Data Source**: {mcp_summary['data_source']}
        - **Agent Involved**: {mcp_summary['agent_involved']}
        - **LLM Call**: {mcp_summary['llm_call']}
        - **External API**: {mcp_summary['external_api']}
        - **Governance**: {mcp_summary['governance']}
        
        **Use Cases**: {', '.join(mcp_summary['use_cases'])}
        """)
    
    st.markdown("---")
    
    # Display diagram
    st.markdown("### 🎨 Numbered Flow Diagram")
    
    if diagram_orientation == "Horizontal (Left to Right)":
        flow_diagram = create_numbered_flow_diagram(flow_param)
    else:
        flow_diagram = create_numbered_flow_diagram_vertical(flow_param)
    
    st.graphviz_chart(flow_diagram)
    
    # Display detailed step-by-step breakdown
    st.markdown("---")
    st.markdown("### 📋 Step-by-Step Breakdown")
    
    tab1, tab2 = st.tabs(["🟢 RAG Flow Steps", "🔵 MCP Flow Steps"])
    
    with tab1:
        st.markdown("#### RAG Knowledge Retrieval Flow (11 Steps)")
        st.markdown("**Use Case**: 'What are your business hours?'")
        
        for i, step in enumerate(RAG_FLOW, 1):
            comp_from = COMPONENTS.get(step['from'], {})
            comp_to = COMPONENTS.get(step['to'], {})
            st.markdown(f"""
            **Step {i}**: {comp_from.get('icon', '')} {comp_from.get('name', step['from'])} → 
            {comp_to.get('icon', '')} {comp_to.get('name', step['to'])}
            - Protocol: {step['label']}
            - Action: {comp_from.get('technical', 'Processing')}
            """)
    
    with tab2:
        st.markdown("#### MCP Tool Call to Accounts API Flow (21 Steps)")
        st.markdown("**Use Case**: 'Check my account balance'")
        
        for i, step in enumerate(MCP_FLOW, 1):
            comp_from = COMPONENTS.get(step['from'], {})
            comp_to = COMPONENTS.get(step['to'], {})
            st.markdown(f"""
            **Step {i}**: {comp_from.get('icon', '')} {comp_from.get('name', step['from'])} → 
            {comp_to.get('icon', '')} {comp_to.get('name', step['to'])}
            - Protocol: {step['label']}
            - Action: {comp_from.get('technical', 'Processing')}
            """)


def show_full_architecture():
    """Display the complete architecture diagram"""
    st.markdown('<div class="sub-header">📊 Full Architecture Diagram</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This diagram shows the complete architecture with all components and their connections.
    Use the filters below to focus on specific aspects.
    """)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_layers = st.multiselect(
            "Show Layers:",
            [layer_info['name'] for layer_info in sorted(LAYERS.values(), key=lambda x: x['order'])],
            default=[layer_info['name'] for layer_info in sorted(LAYERS.values(), key=lambda x: x['order'])]
        )
    
    with col2:
        highlight_component = st.selectbox(
            "Highlight Component:",
            ["None"] + [comp['name'] for comp in COMPONENTS.values()]
        )
    
    with col3:
        diagram_direction = st.selectbox(
            "Diagram Direction:",
            ["Top to Bottom", "Left to Right"],
            index=0
        )
    
    # Export button
    col_export1, col_export2, col_export3 = st.columns([2, 1, 2])
    with col_export2:
        if st.button("📥 Export to Draw.io", use_container_width=True):
            direction_code = "TB" if diagram_direction == "Top to Bottom" else "LR"
            drawio_content = export_to_drawio(show_layers, direction_code)
            st.download_button(
                label="💾 Download .drawio File",
                data=drawio_content,
                file_name="enterprise_architecture.drawio",
                mime="application/xml",
                use_container_width=True
            )
            st.success("✅ Click above to download! Open with draw.io or diagrams.net")
    
    st.markdown("---")
    
    # Generate diagram
    graph = create_architecture_diagram(show_layers, highlight_component, diagram_direction)
    st.graphviz_chart(graph, use_container_width=True)
    
    # Component count by layer
    st.markdown("### 📈 Components by Layer")
    
    layer_counts = {}
    for comp_data in COMPONENTS.values():
        layer_name = LAYERS[comp_data['layer']]['name']
        if layer_name in show_layers:
            layer_counts[layer_name] = layer_counts.get(layer_name, 0) + 1
    
    cols = st.columns(len(layer_counts))
    for i, (layer_name, count) in enumerate(sorted(layer_counts.items())):
        with cols[i]:
            st.metric(layer_name, count)


def classify_intent(query: str) -> str:
    """Simple intent classification based on keywords"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['card', 'credit', 'debit', 'rewards', 'cashback']):
        return 'card'
    elif any(word in query_lower for word in ['loan', 'mortgage', 'borrow', 'financing', 'interest rate']):
        return 'loan'
    elif any(word in query_lower for word in ['invest', 'wealth', 'portfolio', 'stocks', 'bonds', 'retirement']):
        return 'wealth'
    elif any(word in query_lower for word in ['and', 'also', 'plus']) and len(query_lower.split()) > 10:
        return 'multi'
    else:
        return 'general'


def get_path_for_intent(intent: str) -> list:
    """Get the processing path for a given intent"""
    base_path = ["customer", "authentication", "api_gateway", "waf", "rate_limiter",
                 "content_filter", "planner", "memory_manager", "tool_selector", "executor"]
    
    if intent == "card":
        agent_path = ["card_agent", "azure_openai", "mcp_tools", "crm"]
    elif intent == "loan":
        agent_path = ["loan_agent", "azure_openai", "rag_engine"]
    elif intent == "wealth":
        agent_path = ["wealth_agent", "azure_openai", "rag_engine"]
    else:
        agent_path = ["azure_openai"]
    
    end_path = ["critic", "governance", "api_gateway", "customer"]
    
    return base_path + agent_path + end_path


def create_flow_diagram(path: list) -> graphviz.Digraph:
    """Create a flow diagram for a specific path with numbered arrows and protocols"""
    dot = graphviz.Digraph(comment='Request Flow')
    dot.attr(rankdir='LR', splines='ortho', nodesep='0.8', ranksep='1.0')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
    dot.attr('edge', fontsize='9', fontname='Arial')
    
    # Find split point for request/response
    split_point = len(path) // 2
    for i in range(len(path) - 1, -1, -1):
        if path[i] in ['accounts_api', 'cards_api', 'loans_api', 'crm', 'cosmos_db', 'vector_db']:
            split_point = i + 1
            break
    
    # Add nodes with deployment badges
    for i, comp_id in enumerate(path):
        comp_data = COMPONENTS[comp_id]
        
        # Get deployment badge
        deployment_badge = ""
        if comp_id in ENHANCED_DETAILS:
            deployment_type = ENHANCED_DETAILS[comp_id].get('deployment_type', '')
            if 'Container' in deployment_type:
                deployment_badge = " ⭐"
            elif 'Managed' in deployment_type:
                deployment_badge = " ☁️"
            elif deployment_type.startswith('External'):
                deployment_badge = " 🌐"
        
        label = f"{comp_data['icon']}\\n{comp_data['name']}{deployment_badge}"
        
        # Different color for request vs response path
        if i < split_point:
            # Request path - blue border
            dot.node(comp_id + f"_step{i}", label, fillcolor=comp_data['color'], fontcolor='white', penwidth='2', color='#3B82F6')
        else:
            # Response path - green border
            dot.node(comp_id + f"_step{i}", label, fillcolor=comp_data['color'], fontcolor='white', penwidth='2', color='#10B981')
        
        # Add numbered edge to next node
        if i < len(path) - 1:
            # Get protocol for this connection
            protocol_label = ""
            if comp_id in ENHANCED_DETAILS:
                if i < split_point:
                    # Request path - use outbound protocol
                    protocol = ENHANCED_DETAILS[comp_id].get('outbound_protocol', '')
                else:
                    # Response path - use inbound protocol
                    protocol = ENHANCED_DETAILS[comp_id].get('inbound_protocol', '')
                
                if protocol:
                    protocol_label = f"\\n{protocol}"
            
            # Edge label with step number and protocol
            edge_label = f"{i+1}{protocol_label}"
            
            # Different color for request vs response arrows
            if i < split_point - 1:
                # Request arrows - blue
                dot.edge(comp_id + f"_step{i}", path[i + 1] + f"_step{i+1}", label=edge_label, color='#3B82F6', fontcolor='#3B82F6', penwidth='2')
            else:
                # Response arrows - green
                dot.edge(comp_id + f"_step{i}", path[i + 1] + f"_step{i+1}", label=edge_label, color='#10B981', fontcolor='#10B981', penwidth='2')
    
    # Add legend
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', style='filled', color='lightgrey')
        legend.node('legend_request', '➡️ Request Path', shape='plaintext', fillcolor='white')
        legend.node('legend_response', '⬅️ Response Path', shape='plaintext', fillcolor='white')
        legend.node('legend_container', '⭐ = Container (K8s)', shape='plaintext', fillcolor='white')
        legend.node('legend_managed', '☁️ = Managed Service', shape='plaintext', fillcolor='white')
        legend.node('legend_external', '🌐 = External API', shape='plaintext', fillcolor='white')
    
    return dot


def create_architecture_diagram(show_layers: list, highlight_component: str, direction: str) -> graphviz.Digraph:
    """Create the full architecture diagram"""
    dot = graphviz.Digraph(comment='Enterprise Agent Platform Architecture')
    dot.attr(rankdir='TB' if direction == "Top to Bottom" else 'LR', splines='ortho')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    dot.attr('edge', fontsize='8', fontcolor='#6B7280')
    
    # Create subgraphs for each layer
    for layer_id, layer_info in sorted(LAYERS.items(), key=lambda x: x[1]['order']):
        if layer_info['name'] not in show_layers:
            continue
        
        with dot.subgraph(name=f'cluster_{layer_id}') as sub:
            sub.attr(label=layer_info['name'], style='filled', color=layer_info['color'])
            
            # Add components in this layer
            for comp_id, comp_data in COMPONENTS.items():
                if comp_data['layer'] == layer_id:
                    label = f"{comp_data['icon']}\\n{comp_data['name']}"
                    
                    # Highlight if selected
                    if highlight_component != "None" and comp_data['name'] == highlight_component:
                        sub.node(comp_id, label, fillcolor='#FCD34D', fontcolor='#1E3A8A', penwidth='3')
                    else:
                        sub.node(comp_id, label, fillcolor=comp_data['color'], fontcolor='white')
    
    # Add edges
    for flow in FLOWS:
        from_layer = LAYERS[COMPONENTS[flow['from']]['layer']]['name']
        to_layer = LAYERS[COMPONENTS[flow['to']]['layer']]['name']
        
        # Only show edges if both components' layers are visible
        if from_layer in show_layers and to_layer in show_layers:
            # Skip conditional flows for simplicity
            if 'condition' not in flow:
                dot.edge(flow['from'], flow['to'], label=flow['label'])
    
    return dot


# Main content area - execute after all functions are defined
if view_mode == "🏠 Overview":
    show_overview()
elif view_mode == "🔍 Component Explorer":
    show_component_explorer()
elif view_mode == "🧠 Planner Agent Details":
    show_planner_details()
elif view_mode == "🚀 Request Flow Simulator":
    show_request_simulator()
elif view_mode == "🎯 Numbered Flows":
    show_numbered_flows()
elif view_mode == "📊 Full Architecture":
    show_full_architecture()
elif view_mode == "📝 Decision Flow Tables":
    show_decision_flow_tables()
elif view_mode == "🤖 OpenAPI Prompts":
    show_openapi_prompts()
elif view_mode == "📐 High Level Architecture":
    show_high_level_architecture()
elif view_mode == "✈️ Use Case: Airport Transfer":
    show_airport_transfer_use_case()
