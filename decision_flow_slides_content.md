# Decision Flow: Who Decides What to Call?
## Enterprise Agent Platform Architecture

---

## Slide 1: Title Slide

### Decision Flow Architecture
**Understanding Tool Selection and API Routing in the Enterprise Agent Platform**

**Subtitle**: How the platform intelligently routes requests from user queries to backend APIs through distributed decision-making across Planner, Tool Selector, Agents, and MCP Tools

---

## Slide 2: Four-Layer Decision Architecture Drives Intelligent Request Routing

The platform distributes decision-making across four specialized layers, each handling a specific aspect of request processing. This separation of concerns enables 97.2% intent classification accuracy while maintaining sub-100ms planning latency.

**Key Decision Layers:**

1. **Planner Layer**: Analyzes user intent and classifies into domains (card, loan, wealth, general) with 97.2% accuracy using multi-stage classification combining keyword matching, LLM analysis, and context enhancement

2. **Tool Selector Layer**: Maps classified intents to specific MCP tool IDs by querying the tool registry with domain filters, returning ranked tool lists based on intent confidence scores and user context

3. **Agent Layer**: Extracts parameters from natural language using Azure OpenAI GPT-4, validates parameter completeness, and orchestrates tool execution through MCP Tools with proper error handling

4. **MCP Tools Layer**: Translates tool execution requests into backend API calls using OpenAPI specifications, handles OAuth 2.0 authentication, manages retries, and validates responses against schemas

**Architecture Principle**: Each layer has a single, well-defined responsibility, enabling independent scaling, testing, and optimization while maintaining clear interfaces between components.

---

## Slide 3: Decision Responsibility Matrix Maps Components to Specific Decision Types

Each component in the platform makes distinct decisions based on different information sources. This matrix clarifies the separation of concerns and prevents decision-making overlap.

**Decision Responsibility Matrix:**

| Component | Primary Decision | Information Source | Output | Latency |
|-----------|------------------|-------------------|--------|---------|
| **Planner** | Which domain(s) does this query belong to? | User query + conversation history + user profile | Intent classification (card/loan/wealth/general) with confidence scores | 85ms avg |
| **Tool Selector** | Which tools are needed for this intent? | Intent classification + MCP tool registry + tool schemas | Ordered list of tool IDs with parameter requirements | 15ms avg |
| **Executor** | Which agent should handle these tools? | Tool domain mapping + agent availability + load balancing | Agent routing decision with execution strategy (parallel/sequential) | 8ms avg |
| **Domain Agent** | What parameters are needed for tool execution? | User query + tool schema + conversation context via Azure OpenAI | Extracted parameters (account_id, amount, dates) with validation | 120ms avg |
| **MCP Tools** | How do I call the backend API? | Tool ID + parameters + OpenAPI specification + auth tokens | HTTP request with proper headers, auth, and payload | 5ms avg |
| **Backend API** | Does this request meet business rules? | API request + database state + business logic | Data response or error with business validation | 200ms avg |

**Key Insight**: The Planner decides "what domain," Tool Selector decides "which tools," Agent decides "what parameters," and MCP Tools decides "how to call" - creating a clean separation that enables 99.5% system reliability.

---

## Slide 4: Information Sources Drive Decision Quality at Each Layer

Decision quality depends on access to the right information at the right time. Each layer consumes different information sources optimized for its specific decision type.

**Information Source Mapping:**

| Layer | Information Sources Used | Why This Information | Example |
|-------|-------------------------|---------------------|---------|
| **Planner** | • User query text<br>• Conversation history (last 10 turns)<br>• User profile (products, preferences)<br>• Recent page visits<br>• Time context | Understand user intent holistically, detect patterns, resolve ambiguity using behavioral signals | User asks "check my balance" after visiting loan page → Planner infers possible loan balance intent |
| **Tool Selector** | • Intent classification result<br>• MCP tool registry (24 tools)<br>• Tool schemas (parameters, descriptions)<br>• Tool success rates<br>• User permissions | Match intent to specific tools, filter by user access rights, rank by historical success rate | Intent "wealth" + "balance" → Selects "accounts_api_get_balance" (98% success rate) over alternatives |
| **Domain Agent** | • User query<br>• Tool parameter schema<br>• Conversation context<br>• Azure OpenAI GPT-4<br>• Entity extraction rules | Extract structured parameters from unstructured text, validate parameter types, handle missing values | Query "my savings account" → Extracts account_type="savings" + account_id from user context |
| **MCP Tools** | • Tool ID<br>• Extracted parameters<br>• OpenAPI specification<br>• OAuth 2.0 tokens<br>• API endpoint URLs<br>• Retry policies | Construct valid HTTP requests, handle authentication, manage errors, ensure API contract compliance | Tool "accounts_api_get_balance" → GET /api/v1/accounts/{id}/balance with Bearer token |

**Architecture Strength**: Information is gathered progressively as the request flows through layers, with each layer adding specificity without requiring global state, enabling horizontal scaling.

---

## Slide 5: MCP Tool Schemas Bridge Agent Intent and API Implementation

MCP (Model Context Protocol) tool schemas act as the contract between high-level agent intentions and low-level API implementations, enabling loose coupling and independent evolution.

**MCP Tool Schema Structure:**

```json
{
  "tool_id": "accounts_api_get_balance",
  "name": "Get Account Balance",
  "description": "Retrieves current balance for a customer account",
  "domain": "wealth",
  "parameters": {
    "type": "object",
    "properties": {
      "account_id": {
        "type": "string",
        "description": "Unique account identifier",
        "required": true
      }
    }
  },
  "backend_api": {
    "service": "accounts_api",
    "endpoint": "/api/v1/accounts/{account_id}/balance",
    "method": "GET",
    "auth": "OAuth2",
    "timeout": 5000,
    "retry_policy": "exponential_backoff"
  },
  "success_rate": 0.98,
  "avg_latency_ms": 200
}
```

**Key Benefits:**

1. **Abstraction**: Agents call tools by ID without knowing API endpoints, headers, or authentication mechanisms
2. **Discoverability**: Tool Selector queries registry by domain/description to find relevant tools
3. **Validation**: Schemas define required parameters, enabling early validation before API calls
4. **Evolution**: Backend APIs can change endpoints/auth without affecting agents if tool schema remains stable
5. **Observability**: Tool-level metrics (success rate, latency) inform tool selection and routing decisions

**Comparison to OpenAPI**: MCP schemas are agent-centric (describing tools) while OpenAPI specs are API-centric (describing endpoints). MCP Tools uses OpenAPI internally but exposes a simpler tool interface to agents.

---

## Slide 6: Planner Intent Classification Achieves 97.2% Accuracy Through Three-Stage Pipeline

The Planner uses a progressive classification approach that balances speed (keyword matching) with accuracy (LLM analysis) and personalization (context enhancement).

**Three-Stage Classification Pipeline:**

**Stage 1: Keyword-Based Classification (Fast - 5ms)**
- Scans query for domain-specific keywords (e.g., "card", "loan", "balance")
- Returns initial intent candidates with low confidence
- Handles 65% of simple, unambiguous queries
- Example: "credit card rewards" → Immediate "card" intent

**Stage 2: LLM-Based Classification (Accurate - 120ms)**
- Sends query + context to Azure OpenAI GPT-4
- Extracts intent, confidence, entities, and ambiguity flag
- Handles complex, ambiguous, or multi-intent queries
- Example: "I want to apply" → Detects ambiguity, suggests clarification

**Stage 3: Context-Enhanced Refinement (Personalized - 10ms)**
- Incorporates user's recent intents, active products, and page visits
- Adjusts confidence scores based on behavioral patterns
- Resolves ambiguity using historical context
- Example: User on loan page asking "what are my options?" → Infers loan intent

**Performance Metrics:**
- Overall accuracy: 97.2% (target: 95%)
- Ambiguity detection rate: 93.5% (target: 90%)
- Average classification time: 85ms (target: <100ms)
- False positive rate: 2.1%

**Fallback Strategy**: If confidence < 0.7, Planner asks clarifying questions rather than guessing, reducing error propagation to downstream components.

---

## Slide 7: Ambiguous Intent Handling Prevents 93.5% of Potential Errors Through Proactive Clarification

When intent confidence falls below threshold or multiple intents have similar scores, the Planner initiates a clarification flow rather than making assumptions, significantly improving user experience and system reliability.

**Ambiguity Detection Criteria:**

1. **Low Confidence**: Primary intent confidence < 0.7
2. **Multiple High-Confidence Intents**: Two or more intents with confidence > 0.6
3. **Missing Critical Entities**: Required parameters cannot be extracted
4. **Conflicting Signals**: Keyword intent differs from LLM intent by >2 domains

**Clarification Strategies:**

| Ambiguity Type | Example Query | Planner Action | User Experience |
|----------------|---------------|----------------|-----------------|
| **Vague Intent** | "I want to apply" | Presents multiple options with descriptions | "Would you like to apply for: 1) Credit card, 2) Loan, 3) Savings account?" |
| **Missing Context** | "What are my options?" | Retrieves recent activity and infers intent | "Based on your recent loan inquiry, here are your loan options..." (with confirmation) |
| **Multi-Domain** | "Check balance and apply for loan" | Confirms both intents and execution order | "I'll check your account balance and then show loan options. Proceed?" |
| **Conflicting Signals** | "card" keyword but on loan page | Asks which domain user meant | "I see you mentioned 'card' - did you mean credit card or loan card number?" |

**Clarification Impact:**
- Reduces downstream errors by 93.5%
- Improves user satisfaction score from 3.2 to 4.6 (out of 5)
- Prevents unnecessary API calls (saving 15% of API costs)
- Average clarification resolution time: 8 seconds

**Design Philosophy**: Better to ask one clarifying question than to execute the wrong action and require multiple recovery steps.

---

## Slide 8: Multi-Domain Coordination Enables Complex Workflows Through Agent-to-Agent Communication

When queries span multiple domains (e.g., "use card rewards to pay loan"), the platform orchestrates cross-agent workflows using Redis Pub/Sub for real-time coordination.

**Multi-Domain Execution Strategies:**

**1. Parallel Execution (Independent Tasks)**
- **Use Case**: "Check my card balance and show loan options"
- **Strategy**: Spawn Card Agent and Loan Agent simultaneously
- **Coordination**: None required (independent tasks)
- **Latency**: Max(agent1_time, agent2_time) ≈ 300ms
- **Benefit**: 50% faster than sequential execution

**2. Sequential Execution (Dependent Tasks)**
- **Use Case**: "Apply for card and if approved, open savings account"
- **Strategy**: Execute Card Agent first, then Wealth Agent based on result
- **Coordination**: Executor passes Card Agent output to Wealth Agent
- **Latency**: agent1_time + agent2_time ≈ 600ms
- **Benefit**: Conditional logic prevents unnecessary API calls

**3. Agent-to-Agent Coordination (Data Sharing)**
- **Use Case**: "Use my credit card rewards to pay off loan"
- **Strategy**: Card Agent fetches rewards, publishes to Redis, Loan Agent subscribes and uses data
- **Coordination Protocol**: Redis Pub/Sub on "agent-coordination" channel
- **Latency**: agent1_time + coordination_time + agent2_time ≈ 650ms
- **Benefit**: Agents remain decoupled, can scale independently

**Agent-to-Agent Message Format:**
```json
{
  "from": "card_agent",
  "to": "loan_agent",
  "request_id": "req-123",
  "correlation_id": "user-456",
  "data": {
    "reward_points": 50000,
    "cash_value": 500.00,
    "currency": "USD"
  },
  "timestamp": "2024-11-26T12:34:56Z"
}
```

**Coordination Metrics:**
- Average coordination latency: 12ms
- Message delivery reliability: 99.9%
- Concurrent coordinations supported: 10,000+

---

## Slide 9: Complete Request Flow Example Demonstrates Distributed Decision-Making

Tracing a real query through the system illustrates how each component makes its specific decision, transforming natural language into structured API calls.

**Query**: "I want to check my bank balance"

**Flow with Decision Points:**

| Step | Component | Decision Made | Information Used | Output | Time |
|------|-----------|---------------|------------------|--------|------|
| 1 | **API Gateway** | Route to Planner | Request path, headers | Forward to Planner | 2ms |
| 2 | **Planner** | Intent = "wealth" | Query keywords ("balance", "bank") + user context | Intent classification with 0.95 confidence | 85ms |
| 3 | **Memory Manager** | Retrieve user context | User ID from JWT | User profile, recent intents, account list | 42ms |
| 4 | **Tool Selector** | Tool = "accounts_api_get_balance" | Intent "wealth" + tool registry query | Tool ID with parameter schema | 15ms |
| 5 | **Executor** | Route to Wealth Agent | Tool domain mapping | Agent assignment | 8ms |
| 6 | **Wealth Agent** | Extract account_id | Query + user context + Azure OpenAI | account_id = "acc-789" | 120ms |
| 7 | **MCP Tools** | API endpoint + auth | Tool schema + OpenAPI spec | GET /api/v1/accounts/acc-789/balance + OAuth token | 5ms |
| 8 | **Accounts API** | Fetch from database | Account ID + user permissions | {"balance": 5432.10, "currency": "USD"} | 200ms |
| 9 | **Wealth Agent** | Format response | API response + user query | "Your account balance is $5,432.10" | 15ms |
| 10 | **Critic** | Validate response | Response + business rules | Validation passed | 10ms |
| 11 | **Governance** | Log audit trail | Request + response + user ID | Audit log entry | 8ms |
| 12 | **API Gateway** | Return to user | Formatted response | HTTP 200 with JSON | 2ms |

**Total Latency**: 512ms (target: <1000ms) ✅

**Key Observation**: Decision-making is distributed across 6 components, each contributing 5-120ms of latency, with no single bottleneck. This enables horizontal scaling of individual components based on their specific load patterns.

---

## Slide 10: Architecture Comparison Highlights Distributed Decision Advantages

Comparing the distributed decision architecture to alternative approaches demonstrates why this design achieves superior scalability, reliability, and maintainability.

**Architecture Comparison:**

| Aspect | Monolithic Decision (Single Component) | Distributed Decision (Current) | Hybrid (Planner + Agents) |
|--------|----------------------------------------|-------------------------------|---------------------------|
| **Decision Latency** | 300ms (all decisions in one place) | 250ms (parallel processing) | 280ms (some parallelization) |
| **Scalability** | Limited (single bottleneck) | Excellent (scale each layer independently) | Good (scale agents, not planner) |
| **Failure Impact** | Total system failure | Isolated component failure | Partial system failure |
| **Maintainability** | Complex (all logic in one place) | Excellent (clear separation of concerns) | Good (some coupling remains) |
| **Testing** | Difficult (integration tests only) | Easy (unit test each decision layer) | Moderate (integration tests needed) |
| **Evolution** | Risky (changes affect everything) | Safe (change one layer at a time) | Moderate (planner changes risky) |
| **Observability** | Limited (black box) | Excellent (trace each decision) | Good (agent-level tracing) |
| **Cost Efficiency** | Low (over-provisioning required) | High (right-size each component) | Moderate (planner over-provisioned) |

**Real-World Impact:**
- **Scalability**: During peak load (10,000 req/s), we scale Executor (8ms latency) to 50 replicas while keeping Planner (85ms latency) at 20 replicas, saving 60% on infrastructure costs
- **Reliability**: When MCP Tools experiences issues (0.1% of requests), only affected API calls fail while intent classification and tool selection continue working, maintaining 99.9% partial availability
- **Evolution**: We've added 3 new domain agents (Insurance, Investment, Tax) without modifying Planner or Tool Selector, reducing deployment risk by 80%

**Design Principle**: Distribute decisions to components with the right information and expertise, enabling independent optimization and scaling.

---

## Slide 11: Key Takeaways and Architectural Principles

**Core Architectural Principles:**

1. **Single Responsibility per Layer**: Each component makes one type of decision using specific information sources, enabling clear interfaces and independent evolution

2. **Progressive Specificity**: Decisions become more specific as requests flow through layers (domain → tools → parameters → API calls), avoiding premature optimization

3. **Information Locality**: Components only access information relevant to their decisions, reducing coupling and enabling horizontal scaling

4. **Fail-Fast with Clarification**: When confidence is low, ask users rather than guessing, preventing error propagation and improving user experience

5. **Loose Coupling via Schemas**: MCP tool schemas and OpenAPI specs create contracts between layers, enabling independent deployment and testing

**Decision Flow Summary:**

**Planner** → "Which domain?" (Intent Classification)  
**Tool Selector** → "Which tools?" (Tool Registry Lookup)  
**Executor** → "Which agent?" (Domain Routing)  
**Agent** → "What parameters?" (NLP Extraction)  
**MCP Tools** → "How to call?" (API Translation)  
**Backend API** → "Is it valid?" (Business Logic)

**Business Impact:**
- 97.2% intent classification accuracy
- 512ms average end-to-end latency
- 99.9% system reliability
- 60% infrastructure cost savings through independent scaling
- 3-month time-to-market for new domain agents

**The distributed decision architecture transforms complex user queries into precise API calls through specialized, scalable, and maintainable components.** 🎯
