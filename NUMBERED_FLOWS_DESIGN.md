# Numbered Flow Sequences Design
## Color-Coded Architecture Flows

---

## 🎨 Flow Color Coding

### Dark Green Flow - RAG Knowledge Retrieval
**Use Case**: "What are your business hours?"
**Color**: Dark Green (#006400)
**Purpose**: Show knowledge base query flow

### Blue Flow - MCP Tool Call to Accounts API
**Use Case**: "Check my account balance"
**Color**: Blue (#0066CC)
**Purpose**: Show real-time API call flow

---

## 🟢 Dark Green Flow: RAG Knowledge Retrieval

### Complete Flow (Request + Response)

#### Forward Path (Request)
1. **Customer** → Authentication (HTTPS/REST)
2. **Authentication** → API Gateway (JWT Token)
3. **API Gateway** → Planner (HTTP/REST)
4. **Planner** → Tool Selector (Intent: "general_question")
5. **Tool Selector** → RAG Engine (Search knowledge base)
6. **RAG Engine** → Vector DB (Semantic search query)
7. **Vector DB** → RAG Engine (Search results)

#### Backward Path (Response)
8. **RAG Engine** → Tool Selector (Knowledge results)
9. **Tool Selector** → Planner (Formatted answer)
10. **Planner** → API Gateway (Final response)
11. **API Gateway** → Customer (Response)

**Total Steps**: 11
**Color**: Dark Green (#006400)
**Label Format**: "🟢1", "🟢2", "🟢3", etc.

---

## 🔵 Blue Flow: MCP Tool Call to Accounts API

### Complete Flow (Request + Response)

#### Forward Path (Request)
1. **Customer** → Authentication (HTTPS/REST)
2. **Authentication** → API Gateway (JWT Token)
3. **API Gateway** → Planner (HTTP/REST)
4. **Planner** → Memory Manager (Retrieve user context)
5. **Memory Manager** → Planner (User context)
6. **Planner** → Tool Selector (Intent: "account_balance")
7. **Tool Selector** → Executor (Selected tools)
8. **Executor** → Wealth Agent (gRPC)
9. **Wealth Agent** → Azure OpenAI (Extract account_id)
10. **Azure OpenAI** → Wealth Agent (account_id extracted)
11. **Wealth Agent** → MCP Tools (Request: get_account_balance)
12. **MCP Tools** → Accounts API (GET /api/v1/accounts/{id}/balance + OAuth 2.0)
13. **Accounts API** → MCP Tools (Balance data)

#### Backward Path (Response)
14. **MCP Tools** → Wealth Agent (Balance data)
15. **Wealth Agent** → Executor (Formatted response)
16. **Executor** → Critic (Validate response)
17. **Critic** → Governance (Check compliance)
18. **Governance** → Critic (Compliance OK)
19. **Critic** → Planner (Validated response)
20. **Planner** → API Gateway (Final response)
21. **API Gateway** → Customer (Response)

**Total Steps**: 21
**Color**: Blue (#0066CC)
**Label Format**: "🔵1", "🔵2", "🔵3", etc.

---

## 📊 Flow Comparison

| Aspect | RAG Flow (Green) | MCP Flow (Blue) |
|--------|------------------|-----------------|
| **Steps** | 11 | 21 |
| **Latency** | ~200ms | ~512ms |
| **Data Source** | Vector DB (static) | Accounts API (real-time) |
| **Agent Involved** | No | Yes (Wealth Agent) |
| **LLM Call** | No | Yes (Azure OpenAI) |
| **External API** | No | Yes (Accounts API) |
| **Governance** | No | Yes |
| **Use Case** | FAQs, policies | Account data, transactions |

---

## 🎨 Visual Design

### Arrow Colors
- **Dark Green**: #006400 (RAG flow)
- **Blue**: #0066CC (MCP flow)
- **Gray**: #999999 (Other flows, background)

### Number Labels
- **Format**: Circle with number inside
- **RAG**: Green circle with white number
- **MCP**: Blue circle with white number
- **Size**: Small, non-intrusive

### Graphviz Implementation
```dot
// RAG Flow Example
customer -> authentication [label="🟢1" color="#006400" fontcolor="#006400" penwidth=2.5]
authentication -> api_gateway [label="🟢2" color="#006400" fontcolor="#006400" penwidth=2.5]

// MCP Flow Example
customer -> authentication [label="🔵1" color="#0066CC" fontcolor="#0066CC" penwidth=2.5]
authentication -> api_gateway [label="🔵2" color="#0066CC" fontcolor="#0066CC" penwidth=2.5]
```

---

## 🎯 Implementation Strategy

### Option 1: Separate Diagrams
- Create two separate diagrams
- One for RAG flow (green)
- One for MCP flow (blue)
- User can toggle between them

### Option 2: Combined Diagram (RECOMMENDED)
- Show both flows on same diagram
- Use different colors and numbers
- Highlight active flow based on user selection
- Gray out non-active flows

### Option 3: Animated Sequence
- Show flows step-by-step
- Animate one number at a time
- Highlight current step
- Show timing for each step

**Recommended**: Option 2 (Combined Diagram) with Option 3 (Animation) as enhancement

---

## 📋 Flow Definitions for Code

### RAG Flow Steps
```python
RAG_FLOW = [
    {"from": "customer", "to": "authentication", "step": 1, "label": "HTTPS/REST", "color": "#006400"},
    {"from": "authentication", "to": "api_gateway", "step": 2, "label": "JWT Token", "color": "#006400"},
    {"from": "api_gateway", "to": "planner", "step": 3, "label": "HTTP/REST", "color": "#006400"},
    {"from": "planner", "to": "tool_selector", "step": 4, "label": "Intent", "color": "#006400"},
    {"from": "tool_selector", "to": "rag_engine", "step": 5, "label": "Search", "color": "#006400"},
    {"from": "rag_engine", "to": "vector_db", "step": 6, "label": "Query", "color": "#006400"},
    {"from": "vector_db", "to": "rag_engine", "step": 7, "label": "Results", "color": "#006400"},
    {"from": "rag_engine", "to": "tool_selector", "step": 8, "label": "Knowledge", "color": "#006400"},
    {"from": "tool_selector", "to": "planner", "step": 9, "label": "Answer", "color": "#006400"},
    {"from": "planner", "to": "api_gateway", "step": 10, "label": "Response", "color": "#006400"},
    {"from": "api_gateway", "to": "customer", "step": 11, "label": "Response", "color": "#006400"},
]
```

### MCP Flow Steps
```python
MCP_FLOW = [
    {"from": "customer", "to": "authentication", "step": 1, "label": "HTTPS/REST", "color": "#0066CC"},
    {"from": "authentication", "to": "api_gateway", "step": 2, "label": "JWT Token", "color": "#0066CC"},
    {"from": "api_gateway", "to": "planner", "step": 3, "label": "HTTP/REST", "color": "#0066CC"},
    {"from": "planner", "to": "memory_manager", "step": 4, "label": "Context", "color": "#0066CC"},
    {"from": "memory_manager", "to": "planner", "step": 5, "label": "User data", "color": "#0066CC"},
    {"from": "planner", "to": "tool_selector", "step": 6, "label": "Intent", "color": "#0066CC"},
    {"from": "tool_selector", "to": "executor", "step": 7, "label": "Tools", "color": "#0066CC"},
    {"from": "executor", "to": "wealth_agent", "step": 8, "label": "gRPC", "color": "#0066CC"},
    {"from": "wealth_agent", "to": "azure_openai", "step": 9, "label": "Extract", "color": "#0066CC"},
    {"from": "azure_openai", "to": "wealth_agent", "step": 10, "label": "account_id", "color": "#0066CC"},
    {"from": "wealth_agent", "to": "mcp_tools", "step": 11, "label": "get_balance", "color": "#0066CC"},
    {"from": "mcp_tools", "to": "accounts_api", "step": 12, "label": "OAuth 2.0", "color": "#0066CC"},
    {"from": "accounts_api", "to": "mcp_tools", "step": 13, "label": "Balance", "color": "#0066CC"},
    {"from": "mcp_tools", "to": "wealth_agent", "step": 14, "label": "Data", "color": "#0066CC"},
    {"from": "wealth_agent", "to": "executor", "step": 15, "label": "Response", "color": "#0066CC"},
    {"from": "executor", "to": "critic", "step": 16, "label": "Validate", "color": "#0066CC"},
    {"from": "critic", "to": "governance", "step": 17, "label": "Check", "color": "#0066CC"},
    {"from": "governance", "to": "critic", "step": 18, "label": "OK", "color": "#0066CC"},
    {"from": "critic", "to": "planner", "step": 19, "label": "Validated", "color": "#0066CC"},
    {"from": "planner", "to": "api_gateway", "step": 20, "label": "Response", "color": "#0066CC"},
    {"from": "api_gateway", "to": "customer", "step": 21, "label": "Response", "color": "#0066CC"},
]
```

---

## 🎨 Legend Design

```
Flow Legend:
🟢 Dark Green (1-11): RAG Knowledge Retrieval Flow
   Example: "What are your business hours?"
   
🔵 Blue (1-21): MCP Tool Call to Accounts API
   Example: "Check my account balance"
   
⚪ Gray: Other system flows (background)
```

---

## ✅ Implementation Checklist

- [ ] Add RAG_FLOW and MCP_FLOW to architecture_data.py
- [ ] Update create_flow_diagram() to support colored numbered flows
- [ ] Add flow selection dropdown (RAG / MCP / Both)
- [ ] Implement flow highlighting logic
- [ ] Add legend to diagram
- [ ] Test with both flows visible
- [ ] Add animation option (optional enhancement)
- [ ] Update documentation

---

## 🎯 Expected Result

Users will be able to:
1. Select "RAG Flow" to see dark green numbered arrows (1-11)
2. Select "MCP Flow" to see blue numbered arrows (1-21)
3. Select "Both Flows" to see both on same diagram
4. Understand the complete request/response path with numbers
5. Compare the two different data retrieval patterns visually
