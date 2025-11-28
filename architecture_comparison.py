"""
Architecture Comparison Functions
Displays side-by-side comparison of Code-Based vs OpenAPI-Based architectures
"""

import streamlit as st
from openapi_flow_definitions import FLOW_COMPARISON, get_flow_comparison_summary

def show_architecture_comparison():
    """Display comprehensive comparison between code-based and OpenAPI-based architectures"""
    
    st.markdown("## 🔄 Architecture Comparison: Code-Based vs OpenAPI-Based")
    
    # Get comparison summary
    comparison = get_flow_comparison_summary()
    code_based = comparison["code_based"]
    openapi_based = comparison["openapi_based"]
    diff = comparison["difference"]
    
    # High-level metrics comparison
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Steps",
            value=f"{code_based['steps']} (Code)",
            delta=f"+{diff['steps']} (OpenAPI)",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="Latency (ms)",
            value=f"{code_based['latency_ms']}ms (Code)",
            delta=f"+{diff['latency_ms']}ms ({diff['overhead_percentage']}%)",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Components",
            value=f"{code_based['components']} (Code)",
            delta=f"+{diff['components']} (OpenAPI)",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Side-by-side comparison table
    st.markdown("### 📋 Detailed Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 🔵 {code_based['name']}")
        st.markdown(f"**Color**: {code_based['color_name']} ({code_based['color']})")
        
        st.markdown("**✅ Pros:**")
        for pro in code_based['pros']:
            st.markdown(f"- {pro}")
        
        st.markdown("**❌ Cons:**")
        for con in code_based['cons']:
            st.markdown(f"- {con}")
        
        st.markdown("**💡 Best For:**")
        for use_case in code_based['use_cases']:
            st.markdown(f"- {use_case}")
    
    with col2:
        st.markdown(f"#### 🟪 {openapi_based['name']}")
        st.markdown(f"**Color**: {openapi_based['color_name']} ({openapi_based['color']})")
        
        st.markdown("**✅ Pros:**")
        for pro in openapi_based['pros']:
            st.markdown(f"- {pro}")
        
        st.markdown("**❌ Cons:**")
        for con in openapi_based['cons']:
            st.markdown(f"- {con}")
        
        st.markdown("**💡 Best For:**")
        for use_case in openapi_based['use_cases']:
            st.markdown(f"- {use_case}")
    
    st.markdown("---")
    
    # Flow steps comparison
    st.markdown("### 🔀 Flow Steps Comparison")
    
    st.markdown("""
    **Scenario**: User asks "Check my account balance"
    
    Both architectures follow similar patterns but differ in how they discover and call APIs.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔵 Code-Based Flow (21 Steps)")
        st.markdown("""
        **Tool Selection (Steps 6-7):**
        1. Tool Selector → **Hardcoded Tool Registry**
        2. Returns: `["accounts_api_get_balance"]`
        
        **API Call (Steps 12-13):**
        1. Wealth Agent → **MCP Tools** (direct function)
        2. MCP Tools → **Accounts API** (hardcoded endpoint)
        
        **Characteristics:**
        - Direct function calls
        - Hardcoded mappings
        - No schema validation
        - Fast execution
        """)
    
    with col2:
        st.markdown("#### 🟪 OpenAPI-Based Flow (27 Steps)")
        st.markdown("""
        **Tool Selection (Steps 7-10):**
        1. Tool Selector → **OpenAPI Registry**
        2. OpenAPI Registry → **Vector DB** (semantic search)
        3. Vector DB → OpenAPI Registry (matched operations)
        4. OpenAPI Registry → Tool Selector
        
        **API Call (Steps 15-19):**
        1. Wealth Agent → **OpenAPI Client** (dynamic)
        2. OpenAPI Client → **Schema Validator**
        3. Schema Validator → OpenAPI Client (validated)
        4. OpenAPI Client → **Accounts API** (from spec)
        5. Accounts API → OpenAPI Client
        
        **Characteristics:**
        - Dynamic client generation
        - Semantic search for operations
        - Schema validation
        - Slower but flexible
        """)
    
    st.markdown("---")
    
    # New components in OpenAPI architecture
    st.markdown("### 🆕 Additional Components in OpenAPI Architecture")
    
    components_data = [
        {
            "name": "📋 OpenAPI Registry",
            "purpose": "Stores and searches OpenAPI specifications",
            "technology": "Python + FastAPI + Vector DB",
            "overhead": "+50ms (semantic search)"
        },
        {
            "name": "🔌 OpenAPI Client",
            "purpose": "Dynamically generates API clients from specs",
            "technology": "openapi-core + requests",
            "overhead": "+30ms (client generation)"
        },
        {
            "name": "✅ Schema Validator",
            "purpose": "Validates requests/responses against schemas",
            "technology": "jsonschema + openapi-schema-validator",
            "overhead": "+20ms (validation)"
        }
    ]
    
    for comp in components_data:
        with st.expander(f"{comp['name']} - {comp['purpose']}"):
            st.markdown(f"**Technology**: {comp['technology']}")
            st.markdown(f"**Latency Overhead**: {comp['overhead']}")
    
    st.markdown("---")
    
    # Recommendation
    st.markdown("### 💡 Recommendation: Hybrid Approach")
    
    st.success("""
    **Best of Both Worlds:**
    
    1. **Use Code-Based for critical paths**
       - Account balance, transactions (high frequency)
       - Performance-critical operations
       - Well-established internal APIs
    
    2. **Use OpenAPI-Based for new integrations**
       - External partner APIs
       - Experimental features
       - Infrequently used operations
    
    3. **Gradual migration strategy**
       - Start with code-based for speed
       - Add OpenAPI specs alongside
       - Migrate to OpenAPI when stable
    
    **Implementation:**
    ```python
    def select_tools(intent, params):
        # Try code-based first (fast path)
        if intent in HARDCODED_TOOLS:
            return HARDCODED_TOOLS[intent]
        
        # Fall back to OpenAPI (dynamic path)
        return openapi_registry.search_operations(intent)
    ```
    """)
    
    st.markdown("---")
    
    # Decision matrix
    st.markdown("### 🎯 Decision Matrix")
    
    st.markdown("""
    | Criteria | Code-Based | OpenAPI-Based | Winner |
    |----------|------------|---------------|--------|
    | **Performance** | ⚡ 512ms | 🐢 612ms | 🔵 Code-Based |
    | **Flexibility** | 🔒 Rigid | 🔓 Dynamic | 🟪 OpenAPI-Based |
    | **Maintainability** | 🔧 Manual | 🤖 Automatic | 🟪 OpenAPI-Based |
    | **Type Safety** | ✅ Compile-time | ⚠️ Runtime | 🔵 Code-Based |
    | **Scalability** | 📈 Moderate | 📈📈 High | 🟪 OpenAPI-Based |
    | **Debugging** | 🐛 Easy | 🐛🐛 Complex | 🔵 Code-Based |
    | **Documentation** | 📝 Manual | 📚 Auto-generated | 🟪 OpenAPI-Based |
    | **New API Integration** | 🕐 Hours/Days | ⚡ Minutes | 🟪 OpenAPI-Based |
    """)
    
    st.markdown("---")
    
    # Visual flow comparison
    st.markdown("### 🎨 Visual Flow Comparison")
    
    st.info("""
    **How to visualize:**
    
    1. Select "Code-Based (Current Implementation)" to see the blue flow (21 steps)
    2. Select "OpenAPI-Based (Alternative Architecture)" to see the purple flow (27 steps)
    3. Compare the numbered arrows to see where the flows differ
    
    **Key Differences:**
    - Steps 7-10: OpenAPI adds Registry + Vector DB lookup
    - Steps 15-17: OpenAPI adds Client generation + Schema validation
    - Total: +6 steps, +100ms latency
    """)
