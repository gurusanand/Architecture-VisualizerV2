"""
Script to add Kafka event flows to MCP_FLOW in architecture_data.py
"""

# Read the file
with open('architecture_data.py', 'r') as f:
    content = f.read()

# Find the MCP_FLOW definition and add Kafka steps
# We'll add Kafka events after the agent execution

# Add after step 14 (Wealth Agent receives data from MCP Tools)
# Insert Kafka event publishing

import re

# Find the MCP_FLOW section
mcp_flow_pattern = r'(MCP_FLOW = \[.*?{"step": 14,.*?"to": "wealth_agent".*?})'
match = re.search(mcp_flow_pattern, content, re.DOTALL)

if match:
    # Add Kafka event steps after step 14
    kafka_steps = ''',
    # Kafka event streaming (async)
    {"step": "14a", "from": "wealth_agent", "to": "kafka", "label": "Publish Execution Event\\n(async)", "protocol": "Kafka Protocol", "latency": "5ms"},
    {"step": "14b", "from": "kafka", "to": "audit_service", "label": "Stream Event\\n(async)", "protocol": "Kafka Protocol", "latency": "3ms"},
    {"step": "14c", "from": "kafka", "to": "analytics_service", "label": "Stream Event\\n(async)", "protocol": "Kafka Protocol", "latency": "3ms"}'''
    
    # Insert after step 14
    insertion_point = match.end()
    content = content[:insertion_point] + kafka_steps + content[insertion_point:]
    
    print("Added Kafka event steps to MCP_FLOW")
else:
    print("Could not find MCP_FLOW step 14")

# Also add Kafka to governance step (after step 18)
governance_pattern = r'({"step": 18,.*?"to": "governance".*?})'
match = re.search(governance_pattern, content, re.DOTALL)

if match:
    kafka_governance_steps = ''',
    {"step": "18a", "from": "governance", "to": "kafka", "label": "Publish Compliance Alert\\n(async)", "protocol": "Kafka Protocol", "latency": "5ms"}'''
    
    insertion_point = match.end()
    content = content[:insertion_point] + kafka_governance_steps + content[insertion_point:]
    
    print("Added Kafka compliance alert to MCP_FLOW")
else:
    print("Could not find MCP_FLOW step 18")

# Write back
with open('architecture_data.py', 'w') as f:
    f.write(content)

print("Kafka flows added to architecture_data.py")
