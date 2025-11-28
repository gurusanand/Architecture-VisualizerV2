# Enterprise Agent Platform - Detailed Code Analysis

## Database Operations & Data Flow

This document provides a detailed analysis of how each component actually works based on the codebase, including specific database operations, API calls, and data transformations.

---

## 1. Data Storage Architecture

### MongoDB Collections
**Database**: `enterprise_agent_platform`

#### Collections:
1. **`mcp_tools`** - MCP tool registry
   - Stores tool definitions, schemas, configurations
   - Indexed by: `tool_id`, `tool_type`
   
2. **`tool_executions`** - Tool execution logs
   - Tracks every tool invocation
   - Fields: execution_id, tool_id, input_data, output_data, status, duration_ms
   
3. **`memory_episodes`** - Episodic memory (conversation history)
   - TTL indexed - auto-expires based on importance_score
   - Fields: episode_id, user_id, conversation_id, content, timestamp, expires_at
   
4. **`memory_semantic`** - Semantic memory (facts, preferences)
   - Stores embeddings for similarity search
   - Fields: memory_id, user_id, content, embedding (384-dim vector), memory_type
   
5. **`audit_logs`** - Immutable audit trail
   - Every significant event logged
   - Fields: event_id, timestamp, user_id, component, action, input, output, hash

### Redis Data Structures
**Database**: Redis instance

#### Keys:
1. **`ratelimit:{user_id}:{endpoint}`** - Sorted Set
   - Members: request_id
   - Scores: timestamp
   - Used for sliding window rate limiting
   
2. **`session:{session_id}`** - Hash
   - User session state
   - TTL: 30 minutes (sliding)
   
3. **`memory:{user_id}:{memory_id}`** - Hash
   - Cached semantic memories
   - TTL: 1 hour
   
4. **`circuit:{service_name}`** - String
   - Circuit breaker state (OPEN/CLOSED/HALF_OPEN)
   - TTL: Based on recovery timeout

### Azure Cosmos DB
**Database**: `enterprise-agent-platform`

#### Containers:
1. **`conversations`** - Long-term conversation storage
   - Partition key: `user_id`
   - Geo-replicated across regions
   
2. **`audit_events`** - Compliance audit log
   - Partition key: `user_id`
   - Immutable, append-only
   
3. **`user_profiles`** - User information
   - Partition key: `user_id`
   - Includes preferences, settings

### Vector Database (Azure Postgres + pgvector)
**Database**: `vector_store`

#### Tables:
1. **`semantic_memories`**
   - Columns: id, user_id, content, embedding (vector(384)), created_at
   - Index: HNSW index on embedding column
   - Used for: Similarity search on user memories

---

## 2. Component-by-Component Data Flow

### Entry Layer

#### Customer → Authentication → API Gateway

**Authentication Flow:**
```
1. User sends request with credentials
2. AuthenticationService.validate_azure_token()
   - Calls Azure AD API: https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
   - Validates JWT signature
   - Checks token expiration
   
3. Generate internal JWT
   - TokenManager.generate_jwt()
   - Payload: {user_id, roles, permissions, exp}
   - Signed with HS256 + secret key
   
4. Store session in Redis
   - Key: session:{session_id}
   - Data: {user_id, token, created_at, last_accessed}
   - TTL: 1800 seconds (30 minutes, sliding)
```

**API Gateway Processing:**
```
1. Request enters gateway
2. Middleware stack (in order):
   a. CORS Middleware - Add headers
   b. Security Middleware - mTLS verification, security headers
   c. WAF Middleware - Pattern matching for attacks
   d. Content Filter Middleware - Azure Content Safety API call
   e. Request ID Middleware - Generate UUID
   f. Logging Middleware - Log to observability
   
3. Rate Limiting Check:
   - RateLimitManager.check_rate_limit()
   - Redis operation:
     ZREMRANGEBYSCORE ratelimit:{key} 0 {window_start}
     ZCARD ratelimit:{key}
     If count < limit: ZADD ratelimit:{key} {timestamp} {request_id}
   
4. Route to orchestrator
```

---

### Security Layer

#### WAF & Content Filter

**WAF Pattern Matching:**
```python
# From src/security/waf.py
Checks performed:
1. SQL Injection patterns: 
   - ' OR '1'='1
   - UNION SELECT
   - DROP TABLE
   
2. XSS patterns:
   - <script>
   - javascript:
   - onerror=
   
3. Path traversal:
   - ../
   - ..\\
   
4. Command injection:
   - ; rm -rf
   - && cat /etc/passwd
```

**Content Filter API Call:**
```python
# Azure Content Safety API
POST https://contentsafety.cognitiveservices.azure.com/contentsafety/text:analyze
Headers:
  Ocp-Apim-Subscription-Key: {key}
Body:
  {
    "text": "{user_input}",
    "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    "outputType": "FourSeverityLevels"
  }

Response:
  {
    "categoriesAnalysis": [
      {"category": "Hate", "severity": 0},
      ...
    ]
  }

Action: Block if any severity > 2
```

---

### Orchestration Layer

#### Planner Agent

**Database Operations:**
```
1. Retrieve user context from Memory Manager
   - MongoDB query: memory_episodes.find({user_id: X}).sort({timestamp: -1}).limit(10)
   - Redis get: memory:{user_id}:*
   
2. Call LLM for planning
   - Azure OpenAI API:
     POST https://{endpoint}/openai/deployments/gpt-4/chat/completions
     Body: {
       "messages": [
         {"role": "system", "content": "You are a planner..."},
         {"role": "user", "content": "{user_query}"}
       ],
       "temperature": 0.7,
       "max_tokens": 500
     }
   
3. Parse LLM response
   - Extract: task_type, needs_tools, needs_execution
   
4. Store plan in state
   - In-memory state graph (LangGraph)
```

#### Tool Selector Agent

**MCP Tool Selection Process:**
```
1. Retrieve available tools from MongoDB
   - Query: mcp_tools.find({is_enabled: true})
   - Returns: List of tool definitions with schemas
   
2. Semantic search over tool descriptions
   - Generate query embedding: SentenceTransformer.encode(query)
   - Calculate cosine similarity with each tool description embedding
   - Rank tools by similarity score
   
3. Filter by availability
   - Check circuit breaker state in Redis
   - Key: circuit:{tool_name}
   - Skip if state == "OPEN"
   
4. Select top K tools
   - Return: [tool_id_1, tool_id_2, ...]
```

#### Executor

**Agent Execution with Database Operations:**
```
For Card Agent example:

1. Retrieve user profile
   - Cosmos DB query:
     SELECT * FROM c WHERE c.user_id = '{user_id}'
   
2. Retrieve episodic memory
   - MongoDB:
     memory_episodes.find({
       user_id: '{user_id}',
       conversation_id: '{conv_id}'
     }).sort({timestamp: -1}).limit(5)
   
3. Search semantic memory
   - Generate query embedding
   - MongoDB (or Vector DB):
     Find documents where cosine_similarity(query_embedding, doc_embedding) > 0.7
   
4. Call Card Agent
   - Agent prepares prompt with context
   - Calls Azure OpenAI:
     POST /openai/deployments/gpt-4/chat/completions
     Body includes: system prompt, user query, retrieved context
   
5. Execute MCP tools if needed
   - Example: Get account details from CRM
   - MCPExecutor.execute_tool('crm_get_account', {user_id: X})
   
6. Log execution to MongoDB
   - Collection: tool_executions
   - Document: {
       execution_id, tool_id, agent_id,
       input_data, output_data, status,
       started_at, completed_at, duration_ms
     }
```

#### Critic Agent

**Validation Process:**
```
1. Retrieve response from executor
2. Call LLM for validation
   - Azure OpenAI with specific validation prompt
   - Chain-of-Verification:
     a. Generate verification questions
     b. Answer each question
     c. Compare with original response
   
3. Fact-check against knowledge base
   - RAG Engine search for supporting evidence
   - Azure AI Search:
     POST /indexes/knowledge-base/docs/search
     Body: {
       "search": "{claim_to_verify}",
       "top": 5,
       "vectorQueries": [{
         "vector": [embedding],
         "k": 5
       }]
     }
   
4. Calculate confidence score
   - Factors: LLM confidence, fact-check results, consistency
   
5. Store validation result
   - MongoDB: audit_logs collection
   - Includes: validation_details, confidence_score, issues_found
```

---

### Agent Layer

#### Card Agent - Detailed Example

**Complete Flow for "Apply for Credit Card":**

```
1. Agent receives request from Executor
   Input: {
     user_id: "user123",
     query: "I want to apply for a travel rewards card",
     context: {episodic_memory, semantic_memory}
   }

2. Retrieve user financial profile
   a. Call MCP Tool: crm_get_customer
      - Tool: SalesforceTool.search_contact(email)
      - API: GET https://salesforce.com/services/data/v58.0/query
      - Query: SELECT Id, Name, Email, CreditScore FROM Contact WHERE Email = '{email}'
      - Response: {Id: "003xxx", CreditScore: 720}
   
   b. Store in MongoDB tool_executions:
      {
        execution_id: "exec-456",
        tool_id: "crm_get_customer",
        input: {email: "user@example.com"},
        output: {Id: "003xxx", CreditScore: 720},
        duration_ms: 245
      }

3. Search card product catalog (RAG)
   a. Generate query embedding
   b. Azure AI Search:
      POST /indexes/card-products/docs/search
      Body: {
        "search": "travel rewards credit card",
        "filter": "category eq 'travel' and active eq true",
        "top": 5,
        "vectorQueries": [{
          "vector": [query_embedding],
          "k": 5,
          "fields": "description_vector"
        }]
      }
   c. Response: [
        {
          "product_id": "card-travel-01",
          "name": "Premium Travel Rewards",
          "annual_fee": 95,
          "rewards_rate": "3x on travel",
          "min_credit_score": 700
        },
        ...
      ]

4. Check eligibility
   - Compare user credit_score (720) with min_credit_score (700)
   - Check existing cards in CRM
   - Apply business rules

5. Prepare LLM prompt
   System: "You are a credit card specialist..."
   User query: "I want to apply for a travel rewards card"
   Context: {
     user_credit_score: 720,
     eligible_cards: [...],
     user_preferences: {prefers_no_annual_fee: false}
   }

6. Call Azure OpenAI
   POST https://{endpoint}/openai/deployments/gpt-4/chat/completions
   Body: {
     "messages": [system_msg, context_msg, user_msg],
     "temperature": 0.7,
     "max_tokens": 800,
     "functions": [
       {
         "name": "create_card_application",
         "description": "Create a credit card application",
         "parameters": {...}
       }
     ]
   }

7. LLM response includes function call
   {
     "function_call": {
       "name": "create_card_application",
       "arguments": {
         "product_id": "card-travel-01",
         "user_id": "user123",
         "requested_credit_limit": 10000
       }
     }
   }

8. Execute function via MCP Tool
   a. Call: crm_create_case
   b. SalesforceTool.create_case():
      POST https://salesforce.com/services/data/v58.0/sobjects/Case
      Body: {
        "Subject": "Credit Card Application",
        "Description": "Travel Rewards Card Application",
        "ContactId": "003xxx",
        "Priority": "Medium",
        "RecordTypeId": "card_application"
      }
   c. Response: {id: "500xxx", CaseNumber: "00001234"}

9. Store application in MongoDB
   Collection: applications
   Document: {
     application_id: "app-789",
     user_id: "user123",
     product_id: "card-travel-01",
     case_id: "500xxx",
     case_number: "00001234",
     status: "pending",
     created_at: timestamp
   }

10. Update semantic memory
    - MemoryManager.store_semantic_memory():
      Content: "User applied for Premium Travel Rewards card on {date}"
      Type: "fact"
      Embedding: [384-dim vector]
    - MongoDB: memory_semantic.insert_one({...})
    - Redis: HSET memory:user123:mem-xyz content "User applied..."

11. Return response
    {
      success: true,
      message: "Application submitted successfully",
      case_number: "00001234",
      next_steps: "You'll receive a decision within 7-10 business days"
    }
```

---

### Support Services

#### Memory Manager

**Episodic Memory Storage:**
```python
# Store conversation turn
await memory_manager.store_episode(
    user_id="user123",
    conversation_id="conv-456",
    content="User: I want a credit card\nAgent: Let me help you...",
    summary="Credit card inquiry",
    entities=["credit card", "travel rewards"],
    importance_score=0.8
)

# MongoDB operation:
db.memory_episodes.insertOne({
    episode_id: "ep-789",
    user_id: "user123",
    conversation_id: "conv-456",
    content: "...",
    summary: "Credit card inquiry",
    entities: ["credit card", "travel rewards"],
    importance_score: 0.8,
    timestamp: ISODate("2024-01-15T10:30:00Z"),
    expires_at: ISODate("2024-04-15T10:30:00Z")  # 90 days * 0.8
})

# TTL Index ensures automatic deletion after expires_at
```

**Semantic Memory Search:**
```python
# Search for user preferences
memories = await memory_manager.search_semantic_memory(
    user_id="user123",
    query="travel preferences",
    top_k=5
)

# Process:
1. Generate query embedding: [0.123, -0.456, ...]
2. MongoDB aggregation:
   db.memory_semantic.aggregate([
     {$match: {user_id: "user123"}},
     {$addFields: {
       similarity: {
         $let: {
           vars: {
             dotProduct: {$reduce: {
               input: {$zip: {inputs: ["$embedding", query_embedding]}},
               initialValue: 0,
               in: {$add: ["$$value", {$multiply: ["$$this.0", "$$this.1"]}]}
             }}
           },
           in: "$$dotProduct"  # Simplified - actual uses full cosine similarity
         }
       }
     }},
     {$sort: {similarity: -1}},
     {$limit: 5}
   ])

3. Return top 5 matches with similarity scores
```

#### RAG Engine

**Knowledge Base Search:**
```python
# Search company knowledge base
results = await rag_engine.hybrid_search(
    query="credit card annual fees",
    top_k=5,
    vector_weight=0.7,
    keyword_weight=0.3
)

# Azure AI Search operation:
POST https://{search-service}.search.windows.net/indexes/knowledge-base/docs/search
Headers:
  api-key: {key}
  Content-Type: application/json
Body: {
  "search": "credit card annual fees",
  "searchMode": "all",
  "queryType": "semantic",
  "semanticConfiguration": "default",
  "top": 5,
  "select": "chunk_id,text,metadata,score",
  "vectorQueries": [
    {
      "kind": "vector",
      "vector": [0.123, -0.456, ...],  # 384-dim embedding
      "fields": "content_vector",
      "k": 5
    }
  ],
  "scoringProfile": "hybrid-scoring",
  "scoringParameters": [
    "vectorWeight-0.7",
    "keywordWeight-0.3"
  ]
}

Response: {
  "value": [
    {
      "chunk_id": "doc1-chunk3",
      "text": "Annual fees for premium cards range from $95-$550...",
      "metadata": {
        "document_id": "policy-doc-123",
        "section": "fees",
        "last_updated": "2024-01-01"
      },
      "@search.score": 0.89,
      "@search.rerankerScore": 0.94
    },
    ...
  ]
}
```

#### Governance Engine

**Token Cost Tracking:**
```python
# After each LLM call
await governance_engine.track_token_usage(
    user_id="user123",
    model="gpt-4",
    prompt_tokens=150,
    completion_tokens=200,
    total_tokens=350
)

# MongoDB operation:
db.token_usage.insertOne({
    usage_id: "usage-456",
    user_id: "user123",
    agent_id: "card_agent",
    model: "gpt-4",
    prompt_tokens: 150,
    completion_tokens: 200,
    total_tokens: 350,
    cost_usd: 0.0105,  # $0.03/1K prompt + $0.06/1K completion
    timestamp: ISODate("2024-01-15T10:30:00Z")
})

# Aggregation for user budget check:
db.token_usage.aggregate([
  {$match: {
    user_id: "user123",
    timestamp: {$gte: ISODate("2024-01-01")}
  }},
  {$group: {
    _id: "$user_id",
    total_cost: {$sum: "$cost_usd"},
    total_tokens: {$sum: "$total_tokens"}
  }}
])
```

**Audit Logging:**
```python
# Log every significant action
await governance_engine.audit_log(
    user_id="user123",
    component="card_agent",
    action="create_application",
    input_data={...},
    output_data={...}
)

# Cosmos DB operation:
container.create_item({
    "id": "audit-789",
    "event_id": "evt-123",
    "timestamp": "2024-01-15T10:30:00Z",
    "user_id": "user123",
    "session_id": "sess-456",
    "component": "card_agent",
    "action": "create_application",
    "input": {...},
    "output": {...},
    "metadata": {
      "ip_address": "192.168.1.1",
      "user_agent": "Mozilla/5.0..."
    },
    "hash": "sha256:abc123..."  # For integrity verification
})

# Partition key: user_id
# Enables efficient querying and geo-replication
```

---

## 3. External API Integrations

### Azure OpenAI

**Endpoint Configuration:**
```
Base URL: https://{resource-name}.openai.azure.com
API Version: 2023-12-01-preview
Authentication: API Key or Managed Identity
```

**Models Used:**
1. **gpt-4** - Complex reasoning, planning
   - Deployment: gpt-4-deployment
   - Max tokens: 8192
   - Temperature: 0.7
   
2. **gpt-3.5-turbo** - Fast responses
   - Deployment: gpt-35-turbo-deployment
   - Max tokens: 4096
   - Temperature: 0.5
   
3. **text-embedding-ada-002** - Embeddings
   - Deployment: embedding-deployment
   - Dimensions: 1536

**API Call Example:**
```python
import httpx

async def call_openai(messages):
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/gpt-4/chat/completions"
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 800,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body, headers=headers)
        return response.json()
```

### Salesforce CRM

**Authentication:**
```
OAuth 2.0 with JWT Bearer Token Flow
Token endpoint: https://login.salesforce.com/services/oauth2/token
```

**API Operations:**
1. **Search Contact**
   - Endpoint: /services/data/v58.0/query
   - Method: GET
   - Query: SOQL (Salesforce Object Query Language)
   
2. **Create Case**
   - Endpoint: /services/data/v58.0/sobjects/Case
   - Method: POST
   - Body: JSON with case details
   
3. **Update Case**
   - Endpoint: /services/data/v58.0/sobjects/Case/{id}
   - Method: PATCH

### ServiceNow

**Authentication:**
```
Basic Auth (username:password)
Or OAuth 2.0
```

**API Operations:**
1. **Create Incident**
   - Endpoint: /api/now/table/incident
   - Method: POST
   
2. **Get Incident**
   - Endpoint: /api/now/table/incident
   - Method: GET
   - Query: sysparm_query=number={incident_number}

---

## 4. Complete Request Flow Example

### Scenario: "I want to apply for a credit card"

```
Step 1: Entry
├─ Customer sends request via web app
├─ Request: POST /api/v1/chat
├─ Body: {user_id: "user123", message: "I want to apply for a credit card"}
└─ Headers: Authorization: Bearer {jwt_token}

Step 2: Authentication
├─ API Gateway extracts JWT
├─ AuthenticationService.decode_token(jwt)
├─ Validates signature and expiration
├─ Redis: GET session:{session_id}
└─ Returns: {user_id: "user123", roles: ["customer"]}

Step 3: Security Checks
├─ WAF: Check for SQL injection, XSS
├─ Rate Limiter:
│  ├─ Redis: ZREMRANGEBYSCORE ratelimit:user123 0 {window_start}
│  ├─ Redis: ZCARD ratelimit:user123
│  └─ If count < 100: ZADD ratelimit:user123 {timestamp} {request_id}
├─ Content Filter:
│  ├─ POST Azure Content Safety API
│  └─ Check severity levels
└─ All checks passed

Step 4: Orchestration - Planner
├─ Retrieve user context:
│  ├─ MongoDB: memory_episodes.find({user_id: "user123"}).limit(10)
│  └─ Redis: HGETALL memory:user123:*
├─ Call Azure OpenAI (GPT-4):
│  ├─ POST /openai/deployments/gpt-4/chat/completions
│  ├─ Prompt: "Analyze: I want to apply for a credit card"
│  └─ Response: {task_type: "card", needs_tools: true}
└─ Plan: Route to Card Agent with tool support

Step 5: Tool Selector
├─ MongoDB: mcp_tools.find({tool_type: "crm", is_enabled: true})
├─ Semantic search over tool descriptions
├─ Selected tools:
│  ├─ crm_get_customer
│  ├─ crm_create_case
│  └─ rag_search_products
└─ Return tool IDs to executor

Step 6: Executor → Card Agent
├─ Initialize Card Agent
├─ Execute tool: crm_get_customer
│  ├─ MCPExecutor.execute_tool("crm_get_customer", {email: "user@ex.com"})
│  ├─ SalesforceTool.search_contact("user@ex.com")
│  ├─ GET https://salesforce.com/services/data/v58.0/query
│  ├─ Query: SELECT Id, CreditScore FROM Contact WHERE Email = 'user@ex.com'
│  ├─ Response: {Id: "003xxx", CreditScore: 720}
│  └─ MongoDB: tool_executions.insertOne({...})
├─ Execute tool: rag_search_products
│  ├─ RAGEngine.hybrid_search("credit card products")
│  ├─ POST Azure AI Search /indexes/card-products/docs/search
│  ├─ Hybrid search: vector (0.7) + keyword (0.3)
│  └─ Response: [Premium Travel Card, Cash Back Card, ...]
├─ Call Azure OpenAI with context:
│  ├─ POST /openai/deployments/gpt-4/chat/completions
│  ├─ Context: {credit_score: 720, eligible_cards: [...]}
│  └─ Response: Recommend Premium Travel Card + function call
├─ Execute function: create_application
│  ├─ SalesforceTool.create_case(...)
│  ├─ POST https://salesforce.com/services/data/v58.0/sobjects/Case
│  ├─ Body: {Subject: "Card Application", ContactId: "003xxx"}
│  └─ Response: {id: "500xxx", CaseNumber: "00001234"}
└─ Return result to executor

Step 7: Critic Validation
├─ Receive response from Card Agent
├─ Call Azure OpenAI for validation:
│  ├─ POST /openai/deployments/gpt-4/chat/completions
│  ├─ Prompt: "Validate this response for accuracy..."
│  └─ Response: {confidence: 0.92, issues: []}
├─ Fact-check against knowledge base:
│  ├─ Azure AI Search: Verify card details
│  └─ Match found: confidence += 0.05
└─ Final confidence: 0.95 (approved)

Step 8: Governance
├─ Track token usage:
│  ├─ MongoDB: token_usage.insertOne({
│  │    user_id: "user123",
│  │    total_tokens: 850,
│  │    cost_usd: 0.0255
│  │  })
│  └─ Check budget: total_cost < user_limit
├─ Audit log:
│  ├─ Cosmos DB: audit_events.create_item({
│  │    event_id: "evt-789",
│  │    component: "card_agent",
│  │    action: "create_application",
│  │    input: {...},
│  │    output: {...}
│  │  })
│  └─ Partition key: user_id
└─ Compliance check: PII redacted in logs

Step 9: Memory Update
├─ Store episodic memory:
│  ├─ MongoDB: memory_episodes.insertOne({
│  │    episode_id: "ep-456",
│  │    user_id: "user123",
│  │    content: "User applied for Premium Travel Card",
│  │    importance_score: 0.9,
│  │    expires_at: +81 days
│  │  })
│  └─ TTL index will auto-delete after expiration
├─ Store semantic memory:
│  ├─ Generate embedding: [0.123, -0.456, ...]
│  ├─ MongoDB: memory_semantic.insertOne({
│  │    memory_id: "mem-789",
│  │    user_id: "user123",
│  │    content: "Prefers travel rewards cards",
│  │    embedding: [...],
│  │    memory_type: "preference"
│  │  })
│  └─ Redis: HSET memory:user123:mem-789 content "Prefers..."
└─ Memory stored successfully

Step 10: Response
├─ API Gateway formats response
├─ Add headers: X-Request-ID, X-Response-Time
├─ Observability:
│  ├─ Prometheus: http_request_duration_seconds.observe(0.245)
│  ├─ Jaeger: End span with trace_id
│  └─ Grafana: Update dashboard metrics
└─ Return to customer:
    {
      "success": true,
      "message": "Your application has been submitted successfully!",
      "case_number": "00001234",
      "next_steps": "You'll receive a decision within 7-10 business days.",
      "recommended_card": {
        "name": "Premium Travel Rewards",
        "annual_fee": "$95",
        "rewards": "3x points on travel"
      }
    }

Total Duration: 2.45 seconds
Components Involved: 18
Database Operations: 23
API Calls: 7
```

---

## 5. Performance Optimizations

### Caching Strategy
```
L1 (In-Memory): Agent state, session data
L2 (Redis): User profiles, tool results, rate limits
L3 (MongoDB): Historical data, audit logs
```

### Connection Pooling
```python
# MongoDB connection pool
MongoClient(
    max_pool_size=100,
    min_pool_size=10,
    max_idle_time_ms=30000
)

# Redis connection pool
redis.ConnectionPool(
    max_connections=50,
    socket_timeout=5
)

# HTTP client connection pool
httpx.AsyncClient(
    limits=httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    )
)
```

### Async Operations
```
All I/O operations are async:
- Database queries
- API calls
- LLM invocations
- Tool executions

Enables concurrent processing of multiple requests
```

---

This detailed analysis shows exactly how data flows through the system, which databases are accessed, what API calls are made, and how each component processes information.
