# Corrected Request Flow - Account Balance Query

## Issue Identified

The current flow visualization doesn't clearly show that **MCP Tools are called BY the Domain Agents**, not directly by the Planner or Executor.

---

## ✅ CORRECT Flow for Account Balance Query

**User Query**: "What's my account balance?"

### Forward Path (Request):

1. **Customer → API Gateway**
   - Protocol: HTTPS/REST
   - Action: POST /api/v1/chat with query

2. **API Gateway → Authentication**
   - Protocol: HTTPS
   - Action: Validate JWT with Azure AD

3. **API Gateway → Security Checks** (Parallel)
   - WAF: Check for threats
   - Rate Limiter: Check Redis counter
   - Content Filter: Validate content safety

4. **API Gateway → Planner**
   - Protocol: HTTP/REST
   - Action: Route request to orchestrator

5. **Planner → Memory Manager**
   - Protocol: HTTP/REST
   - Action: Retrieve user context
   - Database: MongoDB (`memory_episodes.find({user_id})`)

6. **Planner → Tool Selector**
   - Protocol: HTTP/REST
   - Action: Analyze query and select tools
   - Decision: Need "accounts_api_get_balance" tool

7. **Tool Selector → Executor**
   - Protocol: HTTP/REST
   - Action: Send execution plan with selected tools

8. **Executor → Wealth Agent**
   - Protocol: gRPC (streaming)
   - Action: Send request with context and tool list
   - Message: `AgentRequest{query: "balance", tools: ["accounts_api_get_balance"]}`

9. **Wealth Agent → Azure OpenAI**
   - Protocol: HTTPS/REST
   - Action: Understand query intent and extract parameters
   - Result: Identified need for account_id

10. **Wealth Agent → MCP Tools Manager**
    - Protocol: HTTP/REST
    - Action: Request execution of "accounts_api_get_balance" tool
    - Payload: `{tool_id: "accounts_api_get_balance", params: {account_id: "acc-789"}}`

11. **MCP Tools Manager → Accounts API**
    - Protocol: HTTPS/REST + OAuth 2.0
    - Action: GET /api/v1/accounts/acc-789/balance
    - Headers: `Authorization: Bearer {oauth_token}`

12. **Accounts API → Core Banking System**
    - Protocol: HTTPS/REST or SOAP
    - Action: Fetch real-time balance from mainframe

### Backward Path (Response):

13. **Core Banking System → Accounts API**
    - Response: `{account_id: "acc-789", balance: 5432.10, currency: "USD", available: 5432.10}`

14. **Accounts API → MCP Tools Manager**
    - Protocol: HTTPS response
    - Data: Balance information

15. **MCP Tools Manager → Wealth Agent**
    - Protocol: HTTP response
    - Action: Return tool execution result
    - Logs: MongoDB (`tool_executions.insertOne({...})`)

16. **Wealth Agent → Azure OpenAI** (Optional)
    - Protocol: HTTPS/REST
    - Action: Format response in natural language
    - Input: "Balance is $5,432.10"
    - Output: "Your account balance is $5,432.10. You have full access to these funds."

17. **Wealth Agent → Executor**
    - Protocol: gRPC response stream
    - Action: Return formatted response

18. **Executor → Critic**
    - Protocol: HTTP/REST
    - Action: Validate response quality

19. **Critic → RAG Engine** (Optional)
    - Protocol: HTTP/REST
    - Action: Fact-check if needed (e.g., verify account exists)

20. **Critic → Governance**
    - Protocol: HTTP/REST
    - Action: Log for compliance
    - Database: Cosmos DB (`audit_events.create_item({...})`)

21. **Critic → Executor**
    - Protocol: HTTP response
    - Action: Return validated response

22. **Executor → Planner**
    - Protocol: HTTP response
    - Action: Return final response

23. **Planner → API Gateway**
    - Protocol: HTTP response
    - Action: Return formatted response

24. **API Gateway → Customer**
    - Protocol: HTTPS/REST
    - Response: `{"response": "Your account balance is $5,432.10. You have full access to these funds.", "confidence": 0.95}`

---

## Key Points

### 1. MCP Tools are Called BY Agents
```
❌ WRONG: Planner → MCP Tools → Accounts API
❌ WRONG: Executor → MCP Tools → Accounts API

✅ CORRECT: Executor → Wealth Agent → MCP Tools → Accounts API
```

### 2. Complete Bidirectional Flow
```
Forward:  Customer → ... → Wealth Agent → MCP Tools → Accounts API → Core Banking
Backward: Core Banking → Accounts API → MCP Tools → Wealth Agent → ... → Customer
```

### 3. Agent Responsibilities
- **Planner**: Analyzes intent, retrieves context
- **Tool Selector**: Identifies which tools are needed
- **Executor**: Routes to appropriate domain agent
- **Domain Agent** (Wealth/Card/Loan): 
  - Calls Azure OpenAI for understanding
  - **Calls MCP Tools to fetch data from backend APIs**
  - Formats response
- **MCP Tools**: Executes API calls to backend systems
- **Critic**: Validates response quality

---

## Comparison: Simple vs Complex Queries

### Simple Query (No Backend API Call)
```
Customer → API Gateway → Planner → RAG Engine → Azure OpenAI → Critic → Planner → API Gateway → Customer
```
Example: "What are your business hours?"
- No agent needed
- No MCP Tools needed
- Just search knowledge base

### Complex Query (With Backend API Call)
```
Customer → API Gateway → Planner → Tool Selector → Executor 
  → Domain Agent → Azure OpenAI (understand)
  → Domain Agent → MCP Tools → Domain API (fetch data)
  → Domain API → MCP Tools → Domain Agent (return data)
  → Domain Agent → Executor → Critic → Planner → API Gateway → Customer
```
Example: "What's my account balance?"
- Needs domain agent (Wealth Agent)
- Needs MCP Tools to call Accounts API
- Needs real-time data from backend

---

## Multi-Agent Scenario

**Query**: "Check my card balance and apply for a loan"

### Flow:
```
1. Planner detects two intents: "card_balance" + "loan_application"
2. Tool Selector identifies tools: ["cards_api_get_balance", "loans_api_create_application"]
3. Executor spawns TWO agents in parallel:

   Path A (Card Balance):
   Executor → Card Agent → MCP Tools → Cards API → Card Management System
   Cards API → MCP Tools → Card Agent → Executor

   Path B (Loan Application):
   Executor → Loan Agent → MCP Tools → Loans API → Loan Origination System
   Loans API → MCP Tools → Loan Agent → Executor

4. Executor aggregates both responses
5. Executor → Critic → Planner → API Gateway → Customer
```

### Agent Coordination (Optional):
```
If Card Agent needs loan eligibility info:
  Card Agent publishes to Redis Pub/Sub: "agent-coordination"
  Loan Agent subscribes and responds with eligibility data
  Card Agent uses this for cross-sell recommendation
```

---

## Updated Sample Query Path

### Investment Advice (Corrected)
```python
"Investment Advice": {
    "query": "Should I invest in stocks or bonds given my age and risk tolerance?",
    "intent": "wealth",
    "path": [
        "customer",           # User asks question
        "authentication",     # Validate identity
        "api_gateway",        # Entry point
        "waf",                # Security check
        "rate_limiter",       # Rate limit check
        "content_filter",     # Content safety check
        "planner",            # Analyze intent
        "memory_manager",     # Retrieve user context (age, risk profile)
        "tool_selector",      # Identify needed tools
        "executor",           # Route to agent
        "wealth_agent",       # Process request
        "azure_openai",       # Understand query (by wealth_agent)
        "wealth_agent",       # Back to agent
        "mcp_tools",          # Call MCP Tools (by wealth_agent)
        "accounts_api",       # Fetch account balance
        "mcp_tools",          # Return to MCP Tools
        "wealth_agent",       # Return to agent
        "rag_engine",         # Search investment products (by wealth_agent)
        "wealth_agent",       # Back to agent
        "executor",           # Return to executor
        "critic",             # Validate response
        "governance",         # Log audit trail
        "planner",            # Return to planner
        "api_gateway",        # Return to gateway
        "customer"            # Return to user
    ],
    "explanation": "User authenticated → security checks → planner retrieves risk profile from memory → tool selector identifies need for account data → executor routes to wealth agent → wealth agent calls Azure OpenAI to understand query → wealth agent calls MCP Tools to fetch account balance from Accounts API → wealth agent calls RAG engine to search investment products → wealth agent returns recommendation → critic validates compliance → governance logs audit → response returned to customer."
}
```

---

## Summary

### ✅ Correct Understanding:
1. **Planner** doesn't call MCP Tools directly
2. **Executor** doesn't call APIs directly
3. **Domain Agents** (Card/Loan/Wealth) call MCP Tools
4. **MCP Tools** call Domain APIs (Accounts/Cards/Loans)
5. **Response flows back** through the same path

### Flow Sequence:
```
Planner → Tool Selector → Executor → Domain Agent → MCP Tools → Domain API
                                                                      ↓
Customer ← API Gateway ← Planner ← Critic ← Executor ← Domain Agent ← MCP Tools ← Domain API
```

This is the **correct, complete bidirectional flow**! 🎯
