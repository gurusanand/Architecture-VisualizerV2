"""
Architecture Data Structure
Defines all components, their relationships, and explanations
"""

# Component definitions with technical and layman explanations
COMPONENTS = {
    "customer": {
        "name": "Customer",
        "layer": "entry",
        "technical": "External user or system initiating requests via mobile/web/voice interfaces or IVR systems",
        "layman": "You - the person using the chatbot through your phone, computer, or voice call",
        "color": "#4A90E2",
        "icon": "👤"
    },
    "authentication": {
        "name": "Authentication",
        "layer": "entry",
        "technical": "Azure Active Directory Single Sign-On (SSO) with OAuth 2.0/OIDC protocols for identity verification and JWT token generation",
        "layman": "Security checkpoint that verifies you are who you say you are, like showing your ID at a building entrance",
        "color": "#50C878",
        "icon": "🔐"
    },
    "api_gateway": {
        "name": "API Gateway",
        "layer": "entry",
        "technical": "FastAPI-based gateway implementing request routing, load balancing, mTLS encryption, WAF protection, and rate limiting using sliding window algorithm",
        "layman": "The main entrance door that checks your credentials, ensures you're not a threat, and directs you to the right department",
        "color": "#9B59B6",
        "icon": "🚪"
    },
    "waf": {
        "name": "WAF & Security",
        "layer": "security",
        "technical": "Web Application Firewall with SQL injection prevention, XSS filtering, CSRF protection, and DDoS mitigation",
        "layman": "Security guards that block hackers and malicious attacks before they reach the system",
        "color": "#E74C3C",
        "icon": "🛡️"
    },
    "rate_limiter": {
        "name": "Rate Limiter",
        "layer": "security",
        "technical": "Redis-backed sliding window rate limiting with configurable thresholds per user/IP using sorted sets for time-series tracking",
        "layman": "Traffic controller that prevents any single person from overwhelming the system with too many requests",
        "color": "#F39C12",
        "icon": "⏱️"
    },
    "content_filter": {
        "name": "Content Filter",
        "layer": "security",
        "technical": "Azure Content Safety API integration for prompt injection detection, jailbreak prevention, and toxic content filtering",
        "layman": "Content moderator that blocks inappropriate or harmful messages before processing",
        "color": "#E67E22",
        "icon": "🔍"
    },
    "planner": {
        "name": "Planner Agent",
        "layer": "orchestration",
        "technical": "LangGraph node using GPT-4 to analyze requests, decompose multi-intent queries, and generate execution plans with task routing decisions",
        "layman": "The manager who reads your request and decides which team members need to work on it",
        "color": "#3498DB",
        "icon": "📋"
    },
    "tool_selector": {
        "name": "Tool Selector",
        "layer": "orchestration",
        "technical": "RAG-enhanced agent using semantic search over MCP tool registry to select optimal tools based on query embeddings and historical performance",
        "layman": "The expert who knows which tools and resources are needed to answer your question",
        "color": "#1ABC9C",
        "icon": "🔧"
    },
    "executor": {
        "name": "Executor",
        "layer": "orchestration",
        "technical": "Execution engine that routes tasks to domain-specific agents, manages parallel execution, handles retries with exponential backoff, and aggregates results",
        "layman": "The worker who actually performs the tasks by coordinating with specialized team members",
        "color": "#2ECC71",
        "icon": "⚙️"
    },
    "critic": {
        "name": "Critic Agent",
        "layer": "orchestration",
        "technical": "Hallucination validator using chain-of-verification, fact-checking against knowledge base, confidence scoring, and self-consistency checks",
        "layman": "The quality inspector who checks if the answer is accurate and makes sense before sending it to you",
        "color": "#E91E63",
        "icon": "✓"
    },
    "card_agent": {
        "name": "Card Agent",
        "layer": "agents",
        "technical": "Domain-specific agent for credit card operations with specialized prompts, card product knowledge base, and CRM integration for application processing",
        "layman": "Credit card specialist who helps with card applications, rewards, and account management",
        "color": "#9C27B0",
        "icon": "💳"
    },
    "loan_agent": {
        "name": "Loan Agent",
        "layer": "agents",
        "technical": "Loan processing agent with underwriting logic, risk assessment models, document verification, and integration with loan origination systems",
        "layman": "Loan officer who helps you understand loan options, calculate payments, and process applications",
        "color": "#673AB7",
        "icon": "🏦"
    },
    "wealth_agent": {
        "name": "Wealth Agent",
        "layer": "agents",
        "technical": "Investment advisory agent with portfolio analysis, market data integration, risk profiling, and compliance-checked financial recommendations",
        "layman": "Financial advisor who helps with investments, retirement planning, and wealth management",
        "color": "#3F51B5",
        "icon": "💰"
    },
    "memory_manager": {
        "name": "Memory Manager",
        "layer": "support",
        "technical": "Hybrid memory system with episodic (conversation history in MongoDB with TTL) and semantic (vector embeddings in Redis/Postgres) storage for personalization",
        "layman": "The system's memory that remembers your past conversations and preferences to provide personalized service",
        "color": "#00BCD4",
        "icon": "🧠"
    },
    "rag_engine": {
        "name": "RAG Engine",
        "layer": "support",
        "technical": "Retrieval-Augmented Generation using Azure AI Search with hybrid search (keyword + vector), reranking, and context injection for grounded responses",
        "layman": "Smart search system that finds relevant information from company documents to answer your questions accurately",
        "color": "#009688",
        "icon": "📚"
    },
    "mcp_tools": {
        "name": "MCP Tools",
        "layer": "support",
        "technical": "Model Context Protocol integration for external tool invocation including CRM APIs, calendar systems, email services, and document retrieval",
        "layman": "Collection of tools that connect to other systems like email, calendar, and customer records",
        "color": "#4CAF50",
        "icon": "🛠️"
    },
    "governance": {
        "name": "Governance Engine",
        "layer": "support",
        "technical": "Enterprise governance with token cost tracking, rate policy enforcement, model registry (MRM), PII redaction, and immutable audit logging to Cosmos DB",
        "layman": "Compliance officer that ensures all operations follow company rules, protect privacy, and stay within budget",
        "color": "#FF9800",
        "icon": "⚖️"
    },
    "cosmos_db": {
        "name": "Cosmos DB",
        "layer": "data",
        "technical": "Geo-replicated NoSQL database for audit logs, conversation history, and user profiles with multi-region write capability and automatic failover",
        "layman": "Main database that stores all your conversations and account information across multiple locations for reliability",
        "color": "#FF5722",
        "icon": "💾"
    },
    "redis": {
        "name": "Redis Cache",
        "layer": "data",
        "technical": "In-memory data store for session state, rate limiting counters, circuit breaker state, and hot-path caching with sub-millisecond latency",
        "layman": "Super-fast temporary storage that keeps frequently used information readily available",
        "color": "#DC143C",
        "icon": "⚡"
    },
    "vector_db": {
        "name": "Vector DB",
        "layer": "data",
        "technical": "Azure Postgres with pgvector extension for semantic memory embeddings, enabling similarity search and personalization features",
        "layman": "Specialized database that understands meaning and relationships to find similar information",
        "color": "#795548",
        "icon": "🔢"
    },
    "azure_openai": {
        "name": "Azure OpenAI",
        "layer": "external",
        "technical": "Enterprise LLM service providing GPT-4, GPT-3.5, and embedding models with private endpoints, data residency, and SLA guarantees",
        "layman": "The AI brain that understands your questions and generates intelligent responses",
        "color": "#2196F3",
        "icon": "🤖"
    },
    "crm": {
        "name": "CRM/ServiceNow",
        "layer": "external",
        "technical": "External enterprise systems integration for customer data retrieval, ticket creation, and case management via REST APIs with circuit breaker protection",
        "layman": "Company systems that store customer information and handle service requests",
        "color": "#607D8B",
        "icon": "📊"
    },
    "accounts_api": {
        "name": "Accounts API",
        "layer": "external",
        "technical": "RESTful API for account operations including balance inquiry, transaction history, account details, and statement retrieval from core banking systems with OAuth 2.0 authentication",
        "layman": "Backend system that handles all your account information like balances and transaction history",
        "color": "#546E7A",
        "icon": "🏦"
    },
    "cards_api": {
        "name": "Cards API",
        "layer": "external",
        "technical": "Card management API for credit/debit card operations including application processing, limit changes, rewards tracking, and transaction authorization",
        "layman": "Backend system that manages your credit and debit cards, rewards, and card applications",
        "color": "#5C6BC0",
        "icon": "💳"
    },
    "loans_api": {
        "name": "Loans API",
        "layer": "external",
        "technical": "Loan origination and servicing API for application submission, eligibility checking, payment scheduling, and loan account management",
        "layman": "Backend system that handles loan applications, payments, and loan account information",
        "color": "#7E57C2",
        "icon": "💰"
    },
    "observability": {
        "name": "Observability",
        "layer": "monitoring",
        "technical": "OpenTelemetry instrumentation with Prometheus metrics, Grafana dashboards, Jaeger distributed tracing, and custom SLO monitoring",
        "layman": "Monitoring system that tracks how well everything is working and alerts if something goes wrong",
        "color": "#FFC107",
        "icon": "📈"
    },
    "kafka": {
        "name": "Kafka Broker",
        "layer": "messaging",
        "technical": "Apache Kafka distributed event streaming platform (Confluent 7.5.0) with 6 topics for async communication, CDC events, agent executions, compliance alerts, and external integrations. Supports 10K+ msgs/sec with <10ms latency",
        "layman": "Message delivery system that allows different parts of the system to communicate asynchronously, like an internal postal service",
        "color": "#231F20",
        "icon": "📨"
    },
    "zookeeper": {
        "name": "Zookeeper",
        "layer": "messaging",
        "technical": "Apache Zookeeper coordination service for Kafka cluster management, leader election, and distributed configuration",
        "layman": "Coordinator that keeps Kafka organized and running smoothly",
        "color": "#FF6B35",
        "icon": "🎯"
    },
    "kafka_connect": {
        "name": "Kafka Connect (Debezium)",
        "layer": "messaging",
        "technical": "Debezium CDC connector that captures database changes from MongoDB and SQL databases and streams them to Kafka topics in real-time with <100ms latency",
        "layman": "Change detector that watches databases and notifies other systems when data changes",
        "color": "#00A8E1",
        "icon": "🔄"
    },
    "analytics_service": {
        "name": "Analytics Service",
        "layer": "messaging",
        "technical": "Real-time analytics engine consuming agent execution events from Kafka to generate metrics, trends, and performance insights",
        "layman": "Analytics system that tracks how agents are performing and identifies trends",
        "color": "#4CAF50",
        "icon": "📊"
    },
    "audit_service": {
        "name": "Audit Service",
        "layer": "messaging",
        "technical": "Comprehensive audit trail service consuming all Kafka topics to maintain immutable logs of database changes, agent executions, and compliance events",
        "layman": "Record keeper that tracks every action for compliance and security audits",
        "color": "#FF9800",
        "icon": "📝"
    },
    "openapi_registry": {
        "name": "OpenAPI Registry",
        "layer": "support",
        "technical": "Stores and searches OpenAPI specifications. Uses vector embeddings to match intents with API operations. Provides semantic search across all available APIs.",
        "layman": "A smart catalog that knows about all available APIs and can find the right one based on what you're trying to do.",
        "color": "#7C3AED",
        "icon": "📋"
    },
    "openapi_client": {
        "name": "OpenAPI Client",
        "layer": "support",
        "technical": "Dynamically generates API clients from OpenAPI specifications. Handles request/response serialization, authentication, and protocol details based on spec.",
        "layman": "A universal connector that can talk to any API by reading its instruction manual (OpenAPI spec).",
        "color": "#7C3AED",
        "icon": "🔌"
    },
    "schema_validator": {
        "name": "Schema Validator",
        "layer": "support",
        "technical": "Validates requests and responses against OpenAPI schemas. Ensures data conforms to API contracts before sending and after receiving.",
        "layman": "A quality checker that makes sure we're sending the right information in the right format to APIs.",
        "color": "#7C3AED",
        "icon": "✅"
    },
}

# Flow definitions - how data moves through the system
FLOWS = [
    # Entry flow
    {"from": "customer", "to": "authentication", "label": "Request"},
    {"from": "authentication", "to": "api_gateway", "label": "JWT Token"},
    
    # Security layer
    {"from": "api_gateway", "to": "waf", "label": "Validate"},
    {"from": "api_gateway", "to": "rate_limiter", "label": "Check Limit"},
    {"from": "api_gateway", "to": "content_filter", "label": "Filter Content"},
    
    # Orchestration flow
    {"from": "api_gateway", "to": "planner", "label": "Route Request"},
    {"from": "planner", "to": "tool_selector", "label": "Plan"},
    {"from": "tool_selector", "to": "executor", "label": "Selected Tools"},
    {"from": "executor", "to": "critic", "label": "Results"},
    
    # Agent execution (conditional based on request type)
    {"from": "executor", "to": "card_agent", "label": "Card Query", "condition": "card"},
    {"from": "executor", "to": "loan_agent", "label": "Loan Query", "condition": "loan"},
    {"from": "executor", "to": "wealth_agent", "label": "Wealth Query", "condition": "wealth"},
    
    # Support services (used by multiple components)
    {"from": "planner", "to": "memory_manager", "label": "Retrieve Context"},
    {"from": "executor", "to": "memory_manager", "label": "Store Interaction"},
    {"from": "tool_selector", "to": "rag_engine", "label": "Search Knowledge"},
    {"from": "executor", "to": "mcp_tools", "label": "Invoke Tools"},
    {"from": "api_gateway", "to": "governance", "label": "Audit & Track"},
    {"from": "critic", "to": "governance", "label": "Validate Compliance"},
    
    # Data layer
    {"from": "memory_manager", "to": "cosmos_db", "label": "Store/Retrieve"},
    {"from": "memory_manager", "to": "vector_db", "label": "Semantic Search"},
    {"from": "rate_limiter", "to": "redis", "label": "Counter"},
    {"from": "governance", "to": "cosmos_db", "label": "Audit Log"},
    
    # External services - LLM calls
    {"from": "card_agent", "to": "azure_openai", "label": "LLM Call"},
    {"from": "loan_agent", "to": "azure_openai", "label": "LLM Call"},
    {"from": "wealth_agent", "to": "azure_openai", "label": "LLM Call"},
    {"from": "rag_engine", "to": "azure_openai", "label": "Embeddings"},
    
    # MCP Tools to Domain APIs
    {"from": "mcp_tools", "to": "crm", "label": "CRM API"},
    {"from": "mcp_tools", "to": "accounts_api", "label": "Account API"},
    {"from": "mcp_tools", "to": "cards_api", "label": "Card API"},
    {"from": "mcp_tools", "to": "loans_api", "label": "Loan API"},
    
    # Agent to MCP Tools (specific calls)
    {"from": "card_agent", "to": "mcp_tools", "label": "Get Card Data"},
    {"from": "loan_agent", "to": "mcp_tools", "label": "Get Loan Data"},
    {"from": "wealth_agent", "to": "mcp_tools", "label": "Get Account Data"},
    
    # Response flow - Forward path
    {"from": "card_agent", "to": "executor", "label": "Agent Response"},
    {"from": "loan_agent", "to": "executor", "label": "Agent Response"},
    {"from": "wealth_agent", "to": "executor", "label": "Agent Response"},
    
    # Response flow - Validation and return
    {"from": "critic", "to": "planner", "label": "Validated Response"},
    {"from": "planner", "to": "api_gateway", "label": "Final Response"},
    {"from": "api_gateway", "to": "customer", "label": "Response"},
    
    # Monitoring
    {"from": "api_gateway", "to": "observability", "label": "Metrics"},
    {"from": "executor", "to": "observability", "label": "Traces"},
    
    # Kafka event streaming
    {"from": "zookeeper", "to": "kafka", "label": "Coordination"},
    {"from": "kafka_connect", "to": "kafka", "label": "CDC Events"},
    {"from": "cosmos_db", "to": "kafka_connect", "label": "DB Changes"},
    {"from": "vector_db", "to": "kafka_connect", "label": "DB Changes"},
    {"from": "card_agent", "to": "kafka", "label": "Execution Events"},
    {"from": "loan_agent", "to": "kafka", "label": "Execution Events"},
    {"from": "wealth_agent", "to": "kafka", "label": "Execution Events"},
    {"from": "governance", "to": "kafka", "label": "Compliance Alerts"},
    {"from": "mcp_tools", "to": "kafka", "label": "External Events"},
    {"from": "kafka", "to": "analytics_service", "label": "Agent Events"},
    {"from": "kafka", "to": "audit_service", "label": "All Events"},
    {"from": "kafka", "to": "observability", "label": "Metrics"},
]

# Layer definitions for visual organization
LAYERS = {
    "entry": {"name": "Entry Layer", "color": "#E8F4F8", "order": 1},
    "security": {"name": "Security Layer", "color": "#FFF3E0", "order": 2},
    "orchestration": {"name": "Orchestration Layer", "color": "#E8F5E9", "order": 3},
    "agents": {"name": "Agent Layer", "color": "#F3E5F5", "order": 4},
    "support": {"name": "Support Services", "color": "#E0F2F1", "order": 5},
    "messaging": {"name": "Messaging & Streaming", "color": "#FCE4EC", "order": 6},
    "data": {"name": "Data Layer", "color": "#FFEBEE", "order": 7},
    "external": {"name": "External Services", "color": "#E3F2FD", "order": 8},
    "governance": {"name": "Governance", "color": "#FFF3E0", "order": 9},
    "monitoring": {"name": "Monitoring", "color": "#FFF9C4", "order": 10}
}

# Numbered flow sequences for visualization
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

# Sample queries and their expected paths
SAMPLE_QUERIES = {
    "Card Application": {
        "query": "I want to apply for a new credit card with travel rewards",
        "intent": "card",
        "path": ["customer", "authentication", "api_gateway", "waf", "rate_limiter", 
                 "content_filter", "planner", "memory_manager", "tool_selector", 
                 "executor", "card_agent", "azure_openai", "card_agent", "mcp_tools",
                 "cards_api", "mcp_tools", "card_agent", "mcp_tools", "crm", "mcp_tools",
                 "card_agent", "kafka", "audit_service", "card_agent", "executor", "critic", "governance", "kafka", "planner",
                 "api_gateway", "customer"],
        "explanation": "Request flows through security → planner analyzes intent → tool selector identifies card tools → executor routes to card agent → card agent calls Azure OpenAI for understanding → card agent calls MCP Tools → MCP Tools fetch card products from Cards API → data returns to card agent → card agent calls MCP Tools again → MCP Tools create case in CRM → data returns to card agent → card agent publishes execution event to Kafka → Kafka streams to Audit Service → card agent returns to executor → critic validates → governance logs audit and publishes compliance alert to Kafka → response returned to customer."
    },
    "Loan Inquiry": {
        "query": "What are my options for a home loan with $50,000 down payment?",
        "intent": "loan",
        "path": ["customer", "authentication", "api_gateway", "waf", "rate_limiter",
                 "content_filter", "planner", "memory_manager", "tool_selector",
                 "executor", "loan_agent", "azure_openai", "loan_agent", "mcp_tools",
                 "loans_api", "mcp_tools", "loan_agent", "rag_engine", "loan_agent",
                 "executor", "critic", "governance", "planner", "api_gateway", "customer"],
        "explanation": "Authentication → security checks → planner retrieves user context from memory → tool selector identifies loan tools → executor routes to loan agent → loan agent calls Azure OpenAI to understand query → loan agent calls MCP Tools → MCP Tools fetch eligibility from Loans API → data returns to loan agent → loan agent calls RAG engine for loan products → loan agent returns recommendation → critic validates → governance audits → response returned."
    },
    "Bank Balance Check": {
        "query": "I want to check my bank balance",
        "intent": "account_balance",
        "path": ["customer", "authentication", "api_gateway", "waf", "rate_limiter",
                 "content_filter", "planner", "memory_manager", "tool_selector",
                 "executor", "wealth_agent", "azure_openai", "wealth_agent", "mcp_tools",
                 "accounts_api", "mcp_tools", "wealth_agent", "executor", "critic",
                 "governance", "planner", "api_gateway", "customer"],
        "explanation": "Authentication → security → planner retrieves user context → tool selector identifies 'accounts_api_get_balance' tool → executor routes to wealth agent → wealth agent calls Azure OpenAI to extract account_id → wealth agent calls MCP Tools → MCP Tools fetch real-time balance from Accounts API → data returns to wealth agent → wealth agent formats response → critic validates → governance logs → response returned. NO RAG needed - direct API call for real-time data."
    },
    "Investment Advice": {
        "query": "Should I invest in stocks or bonds given my age and risk tolerance?",
        "intent": "wealth",
        "path": ["customer", "authentication", "api_gateway", "waf", "rate_limiter",
                 "content_filter", "planner", "memory_manager", "tool_selector",
                 "executor", "wealth_agent", "azure_openai", "wealth_agent", "mcp_tools",
                 "accounts_api", "mcp_tools", "wealth_agent", "rag_engine", "wealth_agent",
                 "executor", "critic", "governance", "planner", "api_gateway", "customer"],
        "explanation": "Authentication → security → planner retrieves risk profile from memory → tool selector identifies need for account data AND investment products → executor routes to wealth agent → wealth agent calls Azure OpenAI to understand query → wealth agent calls MCP Tools to fetch current balance from Accounts API (real-time data) → data returns to wealth agent → wealth agent calls RAG engine to search investment products catalog (static knowledge) → wealth agent combines balance + products + risk profile → returns recommendation → critic validates → governance audits → response returned."
    },
    "General Question": {
        "query": "What are your business hours?",
        "intent": "general",
        "path": ["customer", "authentication", "api_gateway", "waf", "rate_limiter",
                 "content_filter", "planner", "rag_engine", "azure_openai", "critic",
                 "planner", "api_gateway", "customer"],
        "explanation": "Simple questions bypass complex orchestration. Request → security checks → planner identifies as general query → RAG engine searches knowledge base → Azure OpenAI formats response → critic validates → response flows back through planner and API gateway to customer."
    },
    "Multi-Intent Query": {
        "query": "I want to check my credit card balance and also apply for a personal loan",
        "intent": "multi",
        "path": ["customer", "authentication", "api_gateway", "waf", "rate_limiter",
                 "content_filter", "planner", "tool_selector", "executor", "card_agent",
                 "mcp_tools", "cards_api", "card_agent", "loan_agent", "mcp_tools", "loans_api",
                 "loan_agent", "executor", "azure_openai", "critic", "governance", "planner",
                 "api_gateway", "customer"],
        "explanation": "Planner detects two intents → executor runs card and loan agents in parallel → card agent calls Cards API via MCP Tools for balance → loan agent calls Loans API via MCP Tools for eligibility → Azure OpenAI synthesizes combined response → critic validates → governance audits → unified response returned to customer."
    }
}
