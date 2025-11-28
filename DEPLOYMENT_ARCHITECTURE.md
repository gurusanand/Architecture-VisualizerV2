
# Deployment Architecture and Message Exchange Protocols

## Component Deployment Types

### Containerized Microservices (Kubernetes Pods)
- **API Gateway** - FastAPI container (3 replicas)
- **Planner Agent** - Python container with LangGraph
- **Tool Selector** - Python container
- **Executor** - Python container with async workers
- **Critic Agent** - Python container
- **Card Agent** - Python container (domain microservice)
- **Loan Agent** - Python container (domain microservice)
- **Wealth Agent** - Python container (domain microservice)
- **Memory Manager** - Python container with embedding model
- **RAG Engine** - Python container with Azure AI Search SDK
- **MCP Tools Manager** - Python container
- **Governance Engine** - Python container

### Managed Services (Azure PaaS)
- **Authentication** - Azure Active Directory (AAD)
- **Redis Cache** - Azure Cache for Redis
- **Cosmos DB** - Azure Cosmos DB
- **Vector DB** - Azure Database for PostgreSQL with pgvector
- **Azure OpenAI** - Azure OpenAI Service
- **Observability** - Azure Monitor + Application Insights

### External APIs (REST/SOAP)
- **CRM/ServiceNow** - External SaaS
- **Accounts API** - Core banking system (REST)
- **Cards API** - Card management system (REST)
- **Loans API** - Loan origination system (REST)

### Security Components (Middleware/Sidecar)
- **WAF** - Azure Application Gateway WAF
- **Rate Limiter** - Middleware in API Gateway
- **Content Filter** - Azure Content Safety API

---

## Message Exchange Protocols

### HTTP/REST
- Customer → API Gateway: HTTPS/REST
- API Gateway → Agents: HTTP/REST (internal)
- Agents → Azure OpenAI: HTTPS/REST
- MCP Tools → External APIs: HTTPS/REST
- All external API calls: HTTPS/REST with OAuth 2.0

### gRPC
- Agent-to-Agent communication: gRPC (high performance)
- Executor → Agents: gRPC for streaming responses
- Observability telemetry: gRPC (OpenTelemetry)

### Redis Pub/Sub
- Agent coordination: Redis Pub/Sub
- Circuit breaker events: Redis Pub/Sub
- Cache invalidation: Redis Pub/Sub

### Message Queue (Optional)
- Async tool execution: Azure Service Bus
- Long-running tasks: Queue-based processing

---

## Agent-to-Agent Communication Patterns

### 1. Sequential Coordination
Planner → Tool Selector → Executor → Critic
- Protocol: HTTP/REST
- Pattern: Request-Response
- Timeout: 30s per hop

### 2. Parallel Execution
Executor → [Card Agent, Loan Agent, Wealth Agent] (parallel)
- Protocol: gRPC streaming
- Pattern: Fan-out / Fan-in
- Timeout: 60s total

### 3. Agent Collaboration (Multi-Agent)
Card Agent ↔ Loan Agent (cross-sell scenario)
- Protocol: gRPC bidirectional streaming
- Pattern: Peer-to-peer with state sharing
- Coordination: Redis Pub/Sub for events

### 4. Memory Sharing
All Agents → Memory Manager
- Protocol: HTTP/REST for reads, gRPC for writes
- Pattern: Shared state with eventual consistency
- Cache: Redis for hot data

---

## Detailed Flow with Protocols

### Request Flow (Customer → System)
1. Customer → API Gateway: **HTTPS/REST** (TLS 1.3, mTLS optional)
2. API Gateway → Authentication: **HTTPS** to Azure AD
3. API Gateway → WAF: **In-process** (middleware)
4. API Gateway → Rate Limiter: **Redis protocol** (RESP3)
5. API Gateway → Content Filter: **HTTPS/REST** to Azure Content Safety
6. API Gateway → Planner: **HTTP/REST** (internal, service mesh)
7. Planner → Memory Manager: **HTTP/REST** (read context)
8. Planner → Tool Selector: **HTTP/REST**
9. Tool Selector → MCP Tools Manager: **HTTP/REST** (query tools)
10. Executor → Domain Agent: **gRPC** (streaming)
11. Domain Agent → Azure OpenAI: **HTTPS/REST** (Azure SDK)
12. Domain Agent → MCP Tools: **HTTP/REST** (invoke tool)
13. MCP Tools → Domain API: **HTTPS/REST** (OAuth 2.0)
14. Domain API → Backend System: **HTTPS/REST** or **SOAP**

### Response Flow (System → Customer)
15. Domain API → MCP Tools: **HTTPS response**
16. MCP Tools → Domain Agent: **HTTP response**
17. Domain Agent → Executor: **gRPC response stream**
18. Executor → Critic: **HTTP/REST**
19. Critic → RAG Engine: **HTTP/REST** (fact-check)
20. Critic → Executor: **HTTP response**
21. Executor → Planner: **HTTP response**
22. Planner → API Gateway: **HTTP response**
23. API Gateway → Customer: **HTTPS/REST response**

### Monitoring Flow (Continuous)
- All components → Observability: **gRPC** (OpenTelemetry)
- Metrics: **Prometheus pull** or **push gateway**
- Logs: **Fluentd** to Azure Monitor
- Traces: **Jaeger** via OpenTelemetry Collector

---

## Agent Coordination Protocols

### Scenario 1: Single Agent Execution
```
Executor sends gRPC request to Card Agent:
  message: AgentRequest {
    request_id: "req-123"
    user_query: "Apply for credit card"
    context: {...}
  }

Card Agent responds via gRPC stream:
  stream: AgentResponse {
    request_id: "req-123"
    status: "processing" | "completed"
    partial_response: "..."
    final_response: "..."
  }
```

### Scenario 2: Multi-Agent Collaboration
```
Executor broadcasts to multiple agents via gRPC:
  parallel_requests: [
    AgentRequest(agent="card", query="..."),
    AgentRequest(agent="loan", query="...")
  ]

Agents coordinate via Redis Pub/Sub:
  channel: "agent-coordination"
  message: {
    "agent_id": "card_agent",
    "status": "needs_loan_info",
    "request_id": "req-123"
  }

Loan Agent responds to channel:
  channel: "agent-coordination"
  message: {
    "agent_id": "loan_agent",
    "response_to": "card_agent",
    "data": {...}
  }
```

### Scenario 3: Human-in-the-Loop Escalation
```
Critic detects low confidence:
  confidence_score: 0.65 (threshold: 0.80)

Critic publishes to Redis:
  channel: "hitl-escalation"
  message: {
    "request_id": "req-123",
    "reason": "low_confidence",
    "requires_human": true
  }

HITL Service subscribes and notifies human:
  protocol: WebSocket to supervisory panel
  message: {
    "alert": "Review required",
    "request": {...},
    "suggested_response": "..."
  }
```

---

## Container Orchestration

### Kubernetes Deployment
```yaml
# Example: Card Agent Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: card-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: card-agent
  template:
    metadata:
      labels:
        app: card-agent
    spec:
      containers:
      - name: card-agent
        image: acr.azurecr.io/card-agent:v1.0
        ports:
        - containerPort: 8080  # HTTP
        - containerPort: 50051 # gRPC
        env:
        - name: AZURE_OPENAI_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: azure-openai
              key: endpoint
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### Service Mesh (Istio)
- mTLS between all microservices
- Traffic management (canary, blue-green)
- Circuit breaking and retry policies
- Distributed tracing injection

---

## Summary Table

| Component | Deployment | Inbound Protocol | Outbound Protocol | Replicas |
|-----------|------------|------------------|-------------------|----------|
| API Gateway | Container | HTTPS/REST | HTTP/REST | 3 |
| Planner | Container | HTTP/REST | HTTP/REST, gRPC | 2 |
| Tool Selector | Container | HTTP/REST | HTTP/REST | 2 |
| Executor | Container | HTTP/REST | gRPC | 3 |
| Critic | Container | HTTP/REST | HTTP/REST | 2 |
| Card Agent | Container | gRPC | HTTPS/REST, gRPC | 3 |
| Loan Agent | Container | gRPC | HTTPS/REST, gRPC | 3 |
| Wealth Agent | Container | gRPC | HTTPS/REST, gRPC | 3 |
| Memory Manager | Container | HTTP/REST | HTTP/REST | 2 |
| RAG Engine | Container | HTTP/REST | HTTPS/REST | 2 |
| MCP Tools | Container | HTTP/REST | HTTPS/REST | 2 |
| Governance | Container | HTTP/REST | HTTP/REST | 2 |
| Authentication | Managed | HTTPS | - | N/A |
| Redis | Managed | RESP3 | - | N/A |
| Cosmos DB | Managed | HTTPS | - | N/A |
| Vector DB | Managed | PostgreSQL | - | N/A |
| Azure OpenAI | Managed | HTTPS/REST | - | N/A |
| Accounts API | External | HTTPS/REST | - | N/A |
| Cards API | External | HTTPS/REST | - | N/A |
| Loans API | External | HTTPS/REST | - | N/A |
| CRM | External | HTTPS/REST | - | N/A |

