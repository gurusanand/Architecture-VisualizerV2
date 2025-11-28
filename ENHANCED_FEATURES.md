# Enhanced Architecture Visualizer - Code-Level Details

## What's New

The architecture visualizer has been enhanced with **detailed code-level implementation information** showing exactly how each component works, which databases it accesses, what functions it calls, and which external APIs it integrates with.

---

## New Features

### 1. Database Operations Display

For each component, you can now see:

#### MongoDB Operations
- **Exact queries** executed by the component
- **Collections** accessed (mcp_tools, memory_episodes, memory_semantic, tool_executions, etc.)
- **Aggregation pipelines** for complex queries
- **Insert/Update/Find** operations with actual field names

**Example - Memory Manager:**
```javascript
memory_episodes.insertOne({episode_id, user_id, content, expires_at})
memory_episodes.find({user_id, importance_score: {$gte: min}}).sort({timestamp: -1})
memory_semantic.aggregate([cosine_similarity_search])
```

#### Redis Operations
- **Key patterns** used (ratelimit:{key}, session:{id}, memory:{user_id}:{memory_id})
- **Data structures** (Sorted Sets, Hashes, Strings)
- **Commands** executed (ZADD, ZCARD, HSET, EXPIRE, etc.)
- **TTL** configurations

**Example - API Gateway:**
```redis
ZREMRANGEBYSCORE ratelimit:{key} 0 {window_start}
ZCARD ratelimit:{key}
ZADD ratelimit:{key} {timestamp} {request_id}
```

#### Cosmos DB Operations
- **SQL queries** for document retrieval
- **Partition keys** used (user_id)
- **Container** names (audit_events, conversations, user_profiles)

**Example - Executor:**
```sql
SELECT * FROM c WHERE c.user_id = '{user_id}'
```

---

### 2. Function-Level Implementation

Each component now shows its **key functions** with descriptions:

**Example - Authentication:**
- `validate_azure_token(token)` - Validates Azure AD JWT
- `generate_jwt(user_data)` - Creates internal JWT
- `decode_token(token)` - Decodes and validates JWT

**Example - Memory Manager:**
- `store_episode()` - Stores episodic memory
- `retrieve_episodes()` - Retrieves recent episodes
- `store_semantic_memory()` - Stores semantic memory with embedding
- `search_semantic_memory()` - Searches using vector similarity

---

### 3. External API Integration Details

See exactly which external services each component calls:

**Example - Card Agent:**
```http
GET https://salesforce.com/services/data/v58.0/query
POST https://salesforce.com/services/data/v58.0/sobjects/Case
POST /indexes/card-products/docs/search
POST /openai/deployments/gpt-4/chat/completions
```

**Example - CRM Tools:**
```http
POST https://{instance}/services/data/v58.0/sobjects/Case
GET https://{instance}/services/data/v58.0/query
POST https://{instance}/api/now/table/incident
```

---

## Components with Enhanced Details

The following **12 components** now have detailed implementation information:

1. **API Gateway** - Redis operations for rate limiting
2. **Authentication** - Azure AD integration + Redis session management
3. **Planner Agent** - MongoDB memory retrieval + OpenAI API calls
4. **Tool Selector** - MongoDB tool registry + circuit breaker checks
5. **Executor** - MongoDB logging + Cosmos DB user profiles
6. **Critic Agent** - MongoDB audit logs + Azure AI Search fact-checking
7. **Card Agent** - Full stack: MongoDB, Cosmos DB, Salesforce, Azure AI Search, OpenAI
8. **Memory Manager** - MongoDB episodic/semantic memory + Redis caching
9. **RAG Engine** - Azure AI Search hybrid search
10. **Governance Engine** - MongoDB token tracking + Cosmos DB audit logging
11. **MCP Tools Manager** - MongoDB tool registry + execution tracking
12. **CRM Tools** - Salesforce and ServiceNow API integrations

---

## How to Use the Enhanced Features

### Step 1: Open Component Explorer
Navigate to **🔍 Component Explorer** in the sidebar.

### Step 2: Select a Component
Expand any component (e.g., "Card Agent", "Memory Manager", "API Gateway").

### Step 3: View Enhanced Details
Scroll down past the technical and layman explanations to see:

#### 💾 Database Operations
- **Databases Used**: List of all databases accessed
- **MongoDB Operations**: Actual queries with collection names
- **Redis Operations**: Commands with key patterns
- **Cosmos DB Operations**: SQL queries

#### ⚙️ Key Functions
- Function names with descriptions
- Shows what each function does

#### 🌐 External API Calls
- Full API endpoints
- HTTP methods
- Service names (Salesforce, ServiceNow, Azure OpenAI, etc.)

---

## Real-World Example: Card Agent

When you expand the **Card Agent** component, you'll see:

### Databases Used
MongoDB, Cosmos DB, Azure AI Search

### MongoDB Operations
```javascript
tool_executions.insertOne({...})
applications.insertOne({application_id, user_id, product_id, case_id})
```

### Cosmos DB Operations
```sql
SELECT * FROM c WHERE c.user_id = '{user_id}'
```

### Key Functions
- `execute(query, state)` - Processes card-related requests

### External API Calls
```http
GET https://salesforce.com/services/data/v58.0/query
POST https://salesforce.com/services/data/v58.0/sobjects/Case
POST /indexes/card-products/docs/search
POST /openai/deployments/gpt-4/chat/completions
```

**This shows exactly how the Card Agent:**
1. Retrieves user profile from Cosmos DB
2. Searches for customer in Salesforce
3. Searches card products in Azure AI Search
4. Calls OpenAI for intelligent response
5. Creates a case in Salesforce
6. Logs everything to MongoDB

---

## Complete Data Flow Visibility

The enhanced visualizer now answers questions like:

### "How does the orchestrator get user context?"
**Answer**: 
- MongoDB: `memory_episodes.find({user_id}).sort({timestamp: -1}).limit(10)`
- Redis: `HGETALL memory:{user_id}:*`

### "Where are MCP tools stored?"
**Answer**: 
- MongoDB collection: `mcp_tools`
- Query: `mcp_tools.find({is_enabled: true})`

### "How does rate limiting work?"
**Answer**: 
- Redis Sorted Set: `ratelimit:{user_id}:{endpoint}`
- Commands:
  - `ZREMRANGEBYSCORE` - Remove old entries
  - `ZCARD` - Count current requests
  - `ZADD` - Add new request

### "How does the Card Agent get account details?"
**Answer**:
1. Calls MCP Tool: `crm_get_customer`
2. Tool executes: `SalesforceTool.search_contact(email)`
3. API call: `GET https://salesforce.com/services/data/v58.0/query`
4. Query: `SELECT Id, CreditScore FROM Contact WHERE Email = '{email}'`
5. Logs to MongoDB: `tool_executions.insertOne({...})`

---

## Technical Documentation

For even more detailed information, see:

- **CODE_ANALYSIS.md** (942 lines) - Complete code-level analysis with:
  - Database schema details
  - Component-by-component function breakdown
  - Complete request flow example (10 steps, 23 database operations, 7 API calls)
  - MongoDB query patterns
  - Redis command patterns
  - Performance optimizations

---

## Benefits of Enhanced Details

### For Developers
- **Understand implementation** without reading code
- **See exact database queries** for optimization
- **Know which APIs** are called for debugging
- **Identify dependencies** between components

### For Architects
- **Validate design decisions** with actual implementation
- **Identify bottlenecks** from database operations
- **Plan scaling** based on data access patterns
- **Document architecture** with real examples

### For DevOps
- **Monitor database performance** knowing exact queries
- **Set up alerts** for specific operations
- **Optimize caching** based on Redis patterns
- **Plan capacity** from API call patterns

### For Security Teams
- **Audit data access** patterns
- **Verify encryption** in transit (mTLS, HTTPS)
- **Check authentication** flows (Azure AD, JWT)
- **Review API security** (tokens, credentials)

---

## Example Use Cases

### Use Case 1: Debugging Slow Responses
**Problem**: Card application requests are slow

**Solution**: Check Card Agent enhanced details
1. See it calls 4 external APIs
2. Identify Salesforce query as bottleneck
3. Optimize by caching contact lookups in Redis
4. Reduce latency from 2.5s to 0.8s

### Use Case 2: Optimizing Memory Usage
**Problem**: High MongoDB load

**Solution**: Check Memory Manager details
1. See it does vector similarity search in MongoDB
2. Identify aggregation pipeline as expensive
3. Migrate to dedicated Vector DB (pgvector)
4. Reduce query time from 500ms to 50ms

### Use Case 3: Scaling Rate Limiting
**Problem**: Redis rate limiter hitting limits

**Solution**: Check API Gateway details
1. See it uses Sorted Sets for sliding window
2. Identify ZCARD operations on every request
3. Implement local cache with periodic sync
4. Reduce Redis ops by 80%

---

## Future Enhancements

Planned additions:
- **Performance metrics** (average query time, API latency)
- **Cost analysis** (database RU consumption, API costs)
- **Dependency graph** (which components depend on which databases)
- **Query optimization suggestions** (indexes, caching opportunities)
- **Real-time monitoring** (live database operation tracking)

---

## Summary

The enhanced visualizer transforms the architecture from a **high-level diagram** to a **code-level implementation guide**. You can now:

✅ See **exact database queries** for each component  
✅ Understand **which functions** do what  
✅ Know **which APIs** are called and when  
✅ Trace **data flow** from input to output  
✅ Debug **performance issues** with real implementation details  
✅ Document **architecture** with concrete examples  

**The visualizer is now a complete technical reference for the Enterprise Agent Platform!**
