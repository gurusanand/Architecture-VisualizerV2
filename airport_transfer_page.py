"""
Airport Transfer Booking Use Case Visualization Page
Shows complete 22-step journey with all components
"""

import streamlit as st
import graphviz
from airport_transfer_flow import AIRPORT_TRANSFER_FLOW
from architecture_data import COMPONENTS

def show_airport_transfer_use_case():
    """Display the Airport Transfer Booking use case page"""
    
    st.title("✈️ Use Case: Airport Transfer Booking Journey")
    
    # Overview
    st.markdown(f"""
    ### Overview
    
    **Scenario**: Customer has booked a flight. The chatbot proactively offers airport transfer booking, 
    then cross-sells travel card updates and points redemption.
    
    - **Duration**: {AIRPORT_TRANSFER_FLOW['duration']}
    - **Total API Calls**: {AIRPORT_TRANSFER_FLOW['api_calls']}
    - **Total Latency**: {AIRPORT_TRANSFER_FLOW['total_latency']} (API calls only)
    - **Components Used**: {AIRPORT_TRANSFER_FLOW['components_used']} out of 34 (76% of architecture)
    """)
    
    # Phases
    st.markdown("### Journey Phases")
    cols = st.columns(4)
    for i, phase in enumerate(AIRPORT_TRANSFER_FLOW['phases']):
        with cols[i]:
            st.metric(
                label=phase['name'],
                value=f"Steps {phase['steps'][0]}-{phase['steps'][-1]}",
                delta=f"{len(phase['steps'])} steps"
            )
            st.caption(phase['description'])
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Complete Flow",
        "🔍 Step-by-Step Details",
        "🏗️ Components Used",
        "🌐 API Calls",
        "📈 Business Metrics"
    ])
    
    with tab1:
        show_complete_flow()
    
    with tab2:
        show_step_by_step_details()
    
    with tab3:
        show_components_used()
    
    with tab4:
        show_api_calls()
    
    with tab5:
        show_business_metrics()


def show_complete_flow():
    """Show the complete 22-step flow diagram"""
    st.subheader("Complete 22-Step Journey")
    
    # Phase filter
    phase_filter = st.multiselect(
        "Filter by Phase",
        options=[p['name'] for p in AIRPORT_TRANSFER_FLOW['phases']],
        default=[p['name'] for p in AIRPORT_TRANSFER_FLOW['phases']]
    )
    
    # Create flow diagram
    dot = graphviz.Digraph(comment='Airport Transfer Booking Flow')
    dot.attr(rankdir='TB', size='12,16')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Get steps for selected phases
    selected_steps = []
    for phase in AIRPORT_TRANSFER_FLOW['phases']:
        if phase['name'] in phase_filter:
            selected_steps.extend(phase['steps'])
    
    # Phase colors
    phase_colors = {
        "Proactive Engagement": "#10B981",
        "Airport Transfer Booking": "#3B82F6",
        "Travel Card Update": "#F59E0B",
        "Points Redemption Upsell": "#8B5CF6"
    }
    
    # Add nodes for each step
    for step in AIRPORT_TRANSFER_FLOW['steps']:
        if step['id'] in selected_steps:
            phase_name = step['phase']
            color = phase_colors.get(phase_name, "#6B7280")
            
            label = f"{step['id']}. {step['title']}\\n"
            label += f"User: {step['user_action'][:40]}...\\n" if len(step['user_action']) > 40 else f"User: {step['user_action']}\\n"
            label += f"Latency: {step['latency']}"
            
            dot.node(f"step_{step['id']}", label, fillcolor=color, fontcolor='white')
    
    # Add edges
    for i in range(len(AIRPORT_TRANSFER_FLOW['steps']) - 1):
        step = AIRPORT_TRANSFER_FLOW['steps'][i]
        next_step = AIRPORT_TRANSFER_FLOW['steps'][i + 1]
        if step['id'] in selected_steps and next_step['id'] in selected_steps:
            dot.edge(f"step_{step['id']}", f"step_{next_step['id']}", 
                    label=step['protocol'], fontsize='8')
    
    st.graphviz_chart(dot)
    
    # Legend
    st.markdown("#### Legend")
    legend_cols = st.columns(4)
    for i, (phase_name, color) in enumerate(phase_colors.items()):
        with legend_cols[i]:
            st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; color:white; text-align:center'>{phase_name}</div>", unsafe_allow_html=True)


def show_step_by_step_details():
    """Show detailed breakdown of each step"""
    st.subheader("Step-by-Step Breakdown")
    
    # Phase selector
    phase_names = [p['name'] for p in AIRPORT_TRANSFER_FLOW['phases']]
    selected_phase = st.selectbox("Select Phase", phase_names)
    
    # Get steps for selected phase
    phase_steps = []
    for phase in AIRPORT_TRANSFER_FLOW['phases']:
        if phase['name'] == selected_phase:
            phase_steps = phase['steps']
            break
    
    # Display steps
    for step in AIRPORT_TRANSFER_FLOW['steps']:
        if step['id'] in phase_steps:
            with st.expander(f"**Step {step['id']}: {step['title']}**", expanded=(step['id'] == phase_steps[0])):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**User Action**: {step['user_action']}")
                    st.markdown(f"**Chatbot Action**: {step['chatbot_action']}")
                    
                    if 'api_call' in step:
                        st.info(f"🌐 **API Call**: {step['api_call']}")
                    
                    st.markdown(f"**Protocol**: {step['protocol']}")
                    st.markdown(f"**Latency**: {step['latency']}")
                
                with col2:
                    st.markdown("**Components**")
                    for comp_id in step['components']:
                        if comp_id in COMPONENTS:
                            comp = COMPONENTS[comp_id]
                            st.markdown(f"- {comp['icon']} {comp['name']}")


def show_components_used():
    """Show all components involved in the use case"""
    st.subheader("Components Involved")
    
    st.markdown(f"**Total**: {len(AIRPORT_TRANSFER_FLOW['component_list'])} components")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Microservices", "8", "AKS Containers")
    with col2:
        st.metric("Databases", "3", "Cosmos, Redis, Vector")
    with col3:
        st.metric("External APIs", "5", "Cards, CRM, Flight, Transfer, Rewards")
    with col4:
        st.metric("Messaging", "2", "Kafka, Audit")
    
    st.markdown("---")
    
    # Group by layer
    layer_components = {}
    for comp_id in AIRPORT_TRANSFER_FLOW['component_list']:
        if comp_id in COMPONENTS:
            comp = COMPONENTS[comp_id]
            layer = comp['layer']
            if layer not in layer_components:
                layer_components[layer] = []
            layer_components[layer].append(comp)
    
    # Display by layer
    for layer, comps in layer_components.items():
        with st.expander(f"**{layer.replace('_', ' ').title()} Layer** ({len(comps)} components)", expanded=True):
            for comp in comps:
                col1, col2, col3 = st.columns([1, 3, 2])
                
                with col1:
                    st.markdown(f"### {comp['icon']}")
                
                with col2:
                    st.markdown(f"**{comp['name']}**")
                    st.caption(comp.get('description', 'No description available'))
                
                with col3:
                    deployment = comp.get('deployment', 'Unknown')
                    if deployment == 'container':
                        st.markdown("⭐ **Container (AKS)**")
                        st.caption("Kubernetes Pod")
                    elif deployment == 'managed':
                        st.markdown("☁️ **Managed Service**")
                        st.caption("Azure PaaS")
                    elif deployment == 'external':
                        st.markdown("🌐 **External API**")
                        st.caption("Backend System")
                    
                    # Show database/storage info
                    comp_id = [k for k, v in COMPONENTS.items() if v == comp][0]
                    if comp_id in ['cosmos_db', 'redis', 'vector_db']:
                        st.info(f"💾 **Database**")
                    elif comp_id == 'kafka':
                        st.info(f"📨 **Message Broker**")


def show_api_calls():
    """Show all external API calls"""
    st.subheader("External API Calls")
    
    st.markdown(f"**Total API Calls**: {len(AIRPORT_TRANSFER_FLOW['api_calls_summary'])}")
    
    # API calls table
    api_data = []
    for api_call in AIRPORT_TRANSFER_FLOW['api_calls_summary']:
        api_data.append({
            "Step": api_call['step'],
            "API": api_call['api'],
            "Method": api_call['method'],
            "Endpoint": api_call['endpoint'],
            "Purpose": api_call['purpose']
        })
    
    st.table(api_data)
    
    # Database operations
    st.markdown("### Database Operations")
    db_data = []
    for db_op in AIRPORT_TRANSFER_FLOW['database_operations']:
        db_data.append({
            "Step": db_op['step'],
            "Database": db_op['db'],
            "Operation": db_op['operation'],
            "Purpose": db_op['purpose']
        })
    
    st.table(db_data)
    
    # Kafka events
    st.markdown("### Kafka Events")
    kafka_data = []
    for event in AIRPORT_TRANSFER_FLOW['kafka_events']:
        kafka_data.append({
            "Step": event['step'],
            "Topic": event['topic'],
            "Purpose": event['purpose']
        })
    
    st.table(kafka_data)


def show_business_metrics():
    """Show business metrics and value"""
    st.subheader("Business Value & Metrics")
    
    metrics = AIRPORT_TRANSFER_FLOW['business_metrics']
    
    # Conversion rates
    st.markdown("### Conversion Rates")
    cols = st.columns(3)
    conversions = metrics['conversion_rates']
    
    with cols[0]:
        st.metric("Airport Transfer", conversions['airport_transfer'], "from proactive offer")
    with cols[1]:
        st.metric("Travel Card Update", conversions['travel_card_update'], "from transfer booking")
    with cols[2]:
        st.metric("Points Redemption", conversions['points_redemption'], "from card update")
    
    # Revenue
    st.markdown("### Revenue Impact")
    cols = st.columns(2)
    revenue = metrics['revenue']
    
    with cols[0]:
        st.metric("Airport Transfer", revenue['airport_transfer'], "per booking")
    with cols[1]:
        st.metric("Points Conversion Value", revenue['points_conversion_value'], "135,000 points")
    
    # Qualitative benefits
    st.markdown("### Additional Benefits")
    st.info(f"**Customer Satisfaction**: {metrics['customer_satisfaction']}")
    st.info(f"**Operational Efficiency**: {metrics['operational_efficiency']}")
    
    # Journey funnel
    st.markdown("### Conversion Funnel")
    st.markdown("""
    ```
    100 users see proactive offer
      ↓ 40% conversion
    40 users book airport transfer
      ↓ 70% conversion
    28 users update travel card
      ↓ 25% conversion
    7 users redeem points
    ```
    """)
    
    st.success("**Overall Success**: 7% of users complete the full journey (all 3 services)")
