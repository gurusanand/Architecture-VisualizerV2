# OpenAPI-Based Flow Design
## Comparison: Code-Based vs OpenAPI-Based Architecture

---

## 🎯 Overview

This document compares two architectural approaches for the Enterprise Agent Platform:

1. **Code-Based Flow** (Current Implementation)
   - MCP tool schemas hardcoded in Python
   - Tool selection via Python logic
   - Direct function calls

2. **OpenAPI-Based Flow** (Alternative Architecture)
   - OpenAPI specs for all APIs
   - Dynamic tool discovery
   - Schema-driven integration

---

## 🔄 Key Differences

### Code-Based Flow (Current)

**Tool Definition:**
```python
# In mcp_tools/tools/accounts_tools.py
class AccountsTools:
    def get_account_balance(self, account_id: str) -> dict:
        """Hardcoded function"""
        response = requests.get(
            f"https://api.example.com/accounts/{account_id}/balance",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        return response.json()
```

**Tool Selection:**
```python
# In agents/tool_selector.py
if intent == "account_balance":
    selected_tools = ["accounts_api_get_balance"]  # Hardcoded
```

**Characteristics:**
- ✅ Fast (no schema parsing)
- ✅ Type-safe (Python types)
- ❌ Requires code changes for new APIs
- ❌ Tight coupling

---

### OpenAPI-Based Flow (Alternative)

**Tool Definition:**
```yaml
# OpenAPI spec at runtime
openapi: 3.0.0
info:
  title: Accounts API
  version: 1.0.0
paths:
  /accounts/{account_id}/balance:
    get:
      operationId: getAccountBalance
      parameters:
        - name: account_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Account balance
          content:
            application/json:
              schema:
                type: object
                properties:
                  balance:
                    type: number
```

**Tool Selection:**
```python
# In agents/tool_selector.py
# Load OpenAPI specs dynamically
openapi_registry = OpenAPIRegistry()
specs = openapi_registry.load_all_specs()

# Match intent to operation
if intent == "account_balance":
    matched_ops = openapi_registry.find_operations(
        description_contains=["balance", "account"]
    )
    selected_tools = [op.operationId for op in matched_ops]
```

**Characteristics:**
- ✅ Dynamic (no code changes for new APIs)
- ✅ Loose coupling
- ✅ Self-documenting
- ❌ Slower (schema parsing overhead)
- ❌ Runtime validation needed

---

## 📊 Flow Comparison: MCP Tool Call

### Code-Based Flow (21 Steps)

1. Customer → Authentication
2. Authentication → API Gateway
3. API Gateway → Planner
4. Planner → Memory Manager
5. Memory Manager → Planner
6. Planner → Tool Selector
7. **Tool Selector → Hardcoded Tool Registry** (Python dict)
8. Tool Selector → Executor
9. Executor → Wealth Agent
10. Wealth Agent → Azure OpenAI
11. Azure OpenAI → Wealth Agent
12. **Wealth Agent → MCP Tools** (Hardcoded function call)
13. **MCP Tools → Accounts API** (Direct HTTP call)
14. Accounts API → MCP Tools
15. MCP Tools → Wealth Agent
16. Wealth Agent → Executor
17. Executor → Critic
18. Critic → Governance
19. Governance → Critic
20. Critic → Planner
21. Planner → API Gateway → Customer

---

### OpenAPI-Based Flow (24 Steps)

1. Customer → Authentication
2. Authentication → API Gateway
3. API Gateway → Planner
4. Planner → Memory Manager
5. Memory Manager → Planner
6. Planner → Tool Selector
7. **Tool Selector → OpenAPI Registry** (Load specs)
8. **OpenAPI Registry → Vector DB** (Search similar operations)
9. **Vector DB → OpenAPI Registry** (Matched operations)
10. **OpenAPI Registry → Tool Selector** (Return matched tools)
11. Tool Selector → Executor
12. Executor → Wealth Agent
13. Wealth Agent → Azure OpenAI
14. Azure OpenAI → Wealth Agent
15. **Wealth Agent → OpenAPI Client** (Dynamic client generation)
16. **OpenAPI Client → Schema Validator** (Validate parameters)
17. **Schema Validator → OpenAPI Client** (Validation OK)
18. **OpenAPI Client → Accounts API** (HTTP call with OpenAPI metadata)
19. Accounts API → OpenAPI Client
20. OpenAPI Client → Wealth Agent
21. Wealth Agent → Executor
22. Executor → Critic
23. Critic → Governance
24. Governance → Critic
25. Critic → Planner
26. Planner → API Gateway → Customer

**Additional Steps:**
- OpenAPI Registry lookup (steps 7-10)
- Schema validation (steps 16-17)
- Dynamic client generation (step 15)

**Total: 26 steps (vs 21 for code-based)**

---

## 🏗️ New Components for OpenAPI Flow

### 1. OpenAPI Registry
- **Purpose**: Store and search OpenAPI specifications
- **Location**: Support Services layer
- **Technology**: Python + FastAPI + Vector DB
- **Functions**:
  - `load_spec(api_name)` - Load OpenAPI spec
  - `search_operations(query)` - Semantic search for operations
  - `get_operation(operation_id)` - Get specific operation
  - `validate_spec(spec)` - Validate OpenAPI spec

### 2. OpenAPI Client Generator
- **Purpose**: Dynamically generate API clients from specs
- **Location**: Support Services layer
- **Technology**: Python + openapi-core
- **Functions**:
  - `generate_client(spec)` - Create client from spec
  - `call_operation(operation_id, params)` - Call API operation
  - `validate_request(operation_id, params)` - Validate before call
  - `validate_response(operation_id, response)` - Validate response

### 3. Schema Validator
- **Purpose**: Validate requests/responses against OpenAPI schemas
- **Location**: Support Services layer
- **Technology**: jsonschema + openapi-schema-validator
- **Functions**:
  - `validate_parameters(schema, params)` - Validate input
  - `validate_response(schema, response)` - Validate output
  - `get_schema(operation_id)` - Get schema for operation

---

## 📋 Detailed Step-by-Step Comparison

### Scenario: "Check my account balance"

#### Code-Based Flow

**Step 6-7: Tool Selection**
```python
# Tool Selector
intent = "account_balance"
# Hardcoded mapping
TOOL_MAPPING = {
    "account_balance": ["accounts_api_get_balance"]
}
selected_tools = TOOL_MAPPING[intent]
```

**Step 12-13: API Call**
```python
# MCP Tools - Hardcoded function
def execute_tool(tool_name, params):
    if tool_name == "accounts_api_get_balance":
        return AccountsTools().get_account_balance(params['account_id'])

# AccountsTools - Direct HTTP call
def get_account_balance(self, account_id):
    return requests.get(f"{BASE_URL}/accounts/{account_id}/balance")
```

---

#### OpenAPI-Based Flow

**Step 7-10: Tool Selection with OpenAPI**
```python
# Tool Selector
intent = "account_balance"

# Load OpenAPI Registry
registry = OpenAPIRegistry()

# Semantic search for matching operations
query_embedding = embed("get account balance")
matched_ops = registry.search_operations(
    embedding=query_embedding,
    top_k=3
)

# matched_ops = [
#     {"operationId": "getAccountBalance", "api": "accounts_api", "score": 0.95},
#     {"operationId": "getBalance", "api": "cards_api", "score": 0.72},
#     ...
# ]

selected_tools = [matched_ops[0]['operationId']]
```

**Step 15-19: API Call with OpenAPI**
```python
# Wealth Agent
operation_id = "getAccountBalance"
params = {"account_id": user_account_id}

# OpenAPI Client Generator
client = OpenAPIClientGenerator()
api_client = client.generate_client(
    spec=registry.get_spec("accounts_api")
)

# Schema Validator
validator = SchemaValidator()
validation_result = validator.validate_parameters(
    operation_id=operation_id,
    params=params
)

if validation_result.valid:
    # Call API
    response = api_client.call_operation(
        operation_id=operation_id,
        parameters=params
    )
    
    # Validate response
    validator.validate_response(
        operation_id=operation_id,
        response=response
    )
```

---

## 🎨 Visual Differences in Diagram

### Code-Based Flow
- **Fewer components**: No OpenAPI Registry, no Schema Validator
- **Direct connections**: Tool Selector → Executor → Agent → MCP Tools → API
- **Simpler**: Fewer steps, less overhead
- **Color**: Keep current blue (#0066CC)

### OpenAPI-Based Flow
- **More components**: + OpenAPI Registry, + OpenAPI Client, + Schema Validator
- **Indirect connections**: Tool Selector → OpenAPI Registry → Vector DB → Tool Selector → ...
- **More complex**: Additional validation and lookup steps
- **Color**: Use purple (#7C3AED) to distinguish from code-based

---

## 📊 Pros & Cons Comparison

### Code-Based Flow

**Pros:**
- ✅ **Fast**: No schema parsing, direct function calls
- ✅ **Type-safe**: Python type hints, compile-time checks
- ✅ **Simple**: Fewer components, easier to debug
- ✅ **Reliable**: No runtime schema failures
- ✅ **Lower latency**: ~512ms for MCP call

**Cons:**
- ❌ **Rigid**: Requires code changes for new APIs
- ❌ **Tight coupling**: Hard dependency on API structure
- ❌ **Manual maintenance**: Update code when APIs change
- ❌ **No self-documentation**: Need separate API docs
- ❌ **Harder to scale**: Each new API needs new code

---

### OpenAPI-Based Flow

**Pros:**
- ✅ **Dynamic**: Add new APIs without code changes
- ✅ **Loose coupling**: Only depends on OpenAPI specs
- ✅ **Self-documenting**: Specs serve as documentation
- ✅ **Automatic validation**: Schema-based validation
- ✅ **Easier to scale**: Just add new specs
- ✅ **Semantic search**: Find APIs by description
- ✅ **Versioning**: Handle multiple API versions

**Cons:**
- ❌ **Slower**: Schema parsing overhead (~+50-100ms)
- ❌ **Complex**: More components, harder to debug
- ❌ **Runtime errors**: Schema validation failures at runtime
- ❌ **Spec quality**: Depends on well-written OpenAPI specs
- ❌ **Higher latency**: ~612ms for MCP call (+100ms)

---

## 🔀 Hybrid Approach (Recommended)

**Best of both worlds:**

1. **Use Code-Based for critical paths**
   - Account balance, transactions (high frequency)
   - Performance-critical operations
   - Well-established APIs

2. **Use OpenAPI-Based for new integrations**
   - External partner APIs
   - Experimental features
   - Infrequently used operations

3. **Gradual migration**
   - Start with code-based
   - Add OpenAPI specs alongside
   - Migrate to OpenAPI when stable

**Implementation:**
```python
# Tool Selector with hybrid approach
def select_tools(intent, params):
    # Try code-based first (fast path)
    if intent in HARDCODED_TOOLS:
        return HARDCODED_TOOLS[intent]
    
    # Fall back to OpenAPI (dynamic path)
    return openapi_registry.search_operations(intent)
```

---

## 🎯 Toggle Switch Implementation

### UI Design

```
┌─────────────────────────────────────┐
│  Flow Architecture:                 │
│  ○ Code-Based (Current)            │
│  ○ OpenAPI-Based (Alternative)     │
│  ○ Hybrid (Recommended)            │
└─────────────────────────────────────┘
```

### Behavior

**Code-Based Selected:**
- Show 21-step MCP flow (blue)
- Highlight: Tool Selector → Executor → Agent → MCP Tools → API
- No OpenAPI components visible

**OpenAPI-Based Selected:**
- Show 26-step MCP flow (purple)
- Highlight: Tool Selector → OpenAPI Registry → Vector DB → ...
- Show OpenAPI Registry, Client, Validator components

**Hybrid Selected:**
- Show both flows side-by-side
- Blue for code-based path
- Purple for OpenAPI-based path
- Indicate decision point (if/else logic)

---

## 📚 Files to Create/Update

### New Files
1. **openapi_flow_definitions.py** - OpenAPI flow steps
2. **OPENAPI_FLOW_DESIGN.md** - This document
3. **openapi_comparison.py** - Comparison logic

### Updated Files
1. **architecture_data.py** - Add OpenAPI components and flows
2. **app.py** - Add toggle switch to flow pages
3. **numbered_flow_diagram.py** - Support OpenAPI flows

---

## ✅ Implementation Checklist

- [ ] Design OpenAPI flow architecture (this document)
- [ ] Create OpenAPI Registry component definition
- [ ] Create OpenAPI Client component definition
- [ ] Create Schema Validator component definition
- [ ] Define OpenAPI-based MCP flow (26 steps)
- [ ] Add toggle switch to Numbered Flows page
- [ ] Add toggle switch to Request Flow Simulator
- [ ] Create comparison table (code vs OpenAPI)
- [ ] Update diagrams to show both flows
- [ ] Add documentation explaining differences
- [ ] Test toggle functionality

---

## 🎯 Expected User Experience

1. **User opens Numbered Flows page**
2. **Sees toggle switch**: Code-Based | OpenAPI-Based | Hybrid
3. **Selects "Code-Based"**: Shows current 21-step flow (blue)
4. **Selects "OpenAPI-Based"**: Shows alternative 26-step flow (purple)
5. **Selects "Hybrid"**: Shows both flows with decision point
6. **Comparison table below**: Shows pros/cons, latency, complexity
7. **Step-by-step breakdown**: Explains each approach

**Benefits:**
- Understand current architecture
- Explore alternative approaches
- Make informed architectural decisions
- See trade-offs visually
- Learn about OpenAPI integration patterns
