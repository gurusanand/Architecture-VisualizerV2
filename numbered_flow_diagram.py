"""
Numbered Flow Diagram Generator
Creates architecture diagrams with numbered, color-coded flows
"""

import graphviz
from architecture_data import COMPONENTS, RAG_FLOW, MCP_FLOW
from openapi_flow_definitions import OPENAPI_MCP_FLOW

def create_numbered_flow_diagram(flow_type: str = "both") -> graphviz.Digraph:
    """
    Create architecture diagram with numbered, color-coded flows
    
    Args:
        flow_type: "rag", "mcp", or "both"
    
    Returns:
        Graphviz Digraph object
    """
    dot = graphviz.Digraph(comment='Numbered Flow Diagram')
    dot.attr(rankdir='LR', splines='ortho', nodesep='1.0', ranksep='1.5')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
    dot.attr('edge', fontsize='10', fontname='Arial Bold')
    
    # Collect all unique components from selected flows
    all_components = set()
    
    if flow_type in ["rag", "both"]:
        for flow in RAG_FLOW:
            all_components.add(flow['from'])
            all_components.add(flow['to'])
    
    # Choose MCP flow based on type
    mcp_flow_data = OPENAPI_MCP_FLOW if flow_type == "mcp_openapi" else MCP_FLOW
    
    if flow_type in ["mcp", "mcp_openapi", "both"]:
        for flow in mcp_flow_data:
            all_components.add(flow['from'])
            all_components.add(flow['to'])
    
    # Add all components as nodes
    for comp_id in all_components:
        if comp_id in COMPONENTS:
            comp_data = COMPONENTS[comp_id]
            label = f"{comp_data['icon']}\\n{comp_data['name']}"
            dot.node(comp_id, label, fillcolor=comp_data['color'], fontcolor='white', penwidth='1.5')
    
    # Add RAG flow edges (dark green)
    if flow_type in ["rag", "both"]:
        for flow_step in RAG_FLOW:
            edge_label = f"🟢 {flow_step['step']}\\n{flow_step['label']}"
            dot.edge(
                flow_step['from'],
                flow_step['to'],
                label=edge_label,
                color=flow_step['color'],
                fontcolor=flow_step['color'],
                penwidth='3.0',
                style='bold'
            )
    
    # Add MCP flow edges (blue)
    if flow_type in ["mcp", "mcp_openapi", "both"]:
        for flow_step in MCP_FLOW:
            edge_label = f"🔵 {flow_step['step']}\\n{flow_step['label']}"
            
            # Check if this edge already exists (from RAG flow)
            # If so, add MCP flow as a parallel edge
            if flow_type == "both":
                # Use constraint=false to allow parallel edges
                dot.edge(
                    flow_step['from'],
                    flow_step['to'],
                    label=edge_label,
                    color=flow_step['color'],
                    fontcolor=flow_step['color'],
                    penwidth='3.0',
                    style='bold',
                    constraint='false'
                )
            else:
                dot.edge(
                    flow_step['from'],
                    flow_step['to'],
                    label=edge_label,
                    color=flow_step['color'],
                    fontcolor=flow_step['color'],
                    penwidth='3.0',
                    style='bold'
                )
    
    # Add legend
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Flow Legend', style='filled', color='lightgrey', fontsize='12')
        
        if flow_type in ["rag", "both"]:
            legend.node('legend_rag', '🟢 Dark Green (1-11): RAG Knowledge Retrieval\\n"What are your business hours?"', 
                       shape='plaintext', fillcolor='white', fontcolor='#006400')
        
        if flow_type in ["mcp", "mcp_openapi", "both"]:
            legend.node('legend_mcp', '🔵 Blue (1-21): MCP Tool Call to Accounts API\\n"Check my account balance"', 
                       shape='plaintext', fillcolor='white', fontcolor='#0066CC')
        
        legend.node('legend_note', 'Numbers show the sequence of steps\\nColors distinguish different flow types', 
                   shape='plaintext', fillcolor='white', fontcolor='#666666')
    
    return dot


def create_numbered_flow_diagram_vertical(flow_type: str = "both") -> graphviz.Digraph:
    """
    Create vertical architecture diagram with numbered flows
    Better for showing complete end-to-end flows
    
    Args:
        flow_type: "rag", "mcp", or "both"
    
    Returns:
        Graphviz Digraph object
    """
    dot = graphviz.Digraph(comment='Numbered Flow Diagram (Vertical)')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='0.8')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
    dot.attr('edge', fontsize='10', fontname='Arial Bold')
    
    # Collect all unique components
    all_components = set()
    
    if flow_type in ["rag", "both"]:
        for flow in RAG_FLOW:
            all_components.add(flow['from'])
            all_components.add(flow['to'])
    
    # Choose MCP flow based on type
    mcp_flow_data = OPENAPI_MCP_FLOW if flow_type == "mcp_openapi" else MCP_FLOW
    
    if flow_type in ["mcp", "mcp_openapi", "both"]:
        for flow in mcp_flow_data:
            all_components.add(flow['from'])
            all_components.add(flow['to'])
    
    # Add all components as nodes
    for comp_id in all_components:
        if comp_id in COMPONENTS:
            comp_data = COMPONENTS[comp_id]
            label = f"{comp_data['icon']} {comp_data['name']}"
            dot.node(comp_id, label, fillcolor=comp_data['color'], fontcolor='white', penwidth='1.5')
    
    # Add RAG flow edges
    if flow_type in ["rag", "both"]:
        for flow_step in RAG_FLOW:
            edge_label = f"🟢{flow_step['step']}: {flow_step['label']}"
            dot.edge(
                flow_step['from'],
                flow_step['to'],
                label=edge_label,
                color=flow_step['color'],
                fontcolor=flow_step['color'],
                penwidth='2.5',
                style='bold'
            )
    
    # Add MCP flow edges
    if flow_type in ["mcp", "mcp_openapi", "both"]:
        for flow_step in MCP_FLOW:
            edge_label = f"🔵{flow_step['step']}: {flow_step['label']}"
            dot.edge(
                flow_step['from'],
                flow_step['to'],
                label=edge_label,
                color=flow_step['color'],
                fontcolor=flow_step['color'],
                penwidth='2.5',
                style='bold',
                constraint='false' if flow_type == "both" else 'true'
            )
    
    # Add legend at bottom
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Flow Legend', style='filled', color='lightgrey', fontsize='11')
        
        if flow_type in ["rag", "both"]:
            legend.node('legend_rag', '🟢 RAG Flow (11 steps): Knowledge retrieval from vector database', 
                       shape='plaintext', fillcolor='white', fontcolor='#006400')
        
        if flow_type in ["mcp", "mcp_openapi", "both"]:
            legend.node('legend_mcp', '🔵 MCP Flow (21 steps): Real-time API call to Accounts API', 
                       shape='plaintext', fillcolor='white', fontcolor='#0066CC')
    
    return dot


def get_flow_summary(flow_type: str) -> dict:
    """
    Get summary statistics for a flow
    
    Args:
        flow_type: "rag" or "mcp"
    
    Returns:
        Dictionary with flow statistics
    """
    if flow_type == "rag":
        return {
            "name": "RAG Knowledge Retrieval",
            "color": "🟢 Dark Green",
            "steps": 11,
            "latency": "~200ms",
            "data_source": "Vector DB (static knowledge)",
            "agent_involved": "No",
            "llm_call": "No",
            "external_api": "No",
            "governance": "No",
            "use_cases": ["FAQs", "Policies", "Product information", "Business hours"]
        }
    elif flow_type == "mcp":
        return {
            "name": "MCP Tool Call to Accounts API",
            "color": "🔵 Blue",
            "steps": 21,
            "latency": "~512ms",
            "data_source": "Accounts API (real-time data)",
            "agent_involved": "Yes (Wealth Agent)",
            "llm_call": "Yes (Azure OpenAI)",
            "external_api": "Yes (Accounts API)",
            "governance": "Yes",
            "use_cases": ["Account balance", "Transactions", "Account details", "Real-time data"]
        }
    else:
        return {}
