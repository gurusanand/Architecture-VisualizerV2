"""
OpenAPI-Based Flow Definitions
Alternative architecture using OpenAPI specs for dynamic tool discovery
"""

# OpenAPI-based MCP flow (26 steps - adds OpenAPI Registry, Client, Validator)
OPENAPI_MCP_FLOW = [
    # Forward path - with OpenAPI components
    {"from": "customer", "to": "authentication", "step": 1, "label": "HTTPS/REST", "color": "#7C3AED"},
    {"from": "authentication", "to": "api_gateway", "step": 2, "label": "JWT Token", "color": "#7C3AED"},
    {"from": "api_gateway", "to": "planner", "step": 3, "label": "HTTP/REST", "color": "#7C3AED"},
    {"from": "planner", "to": "memory_manager", "step": 4, "label": "Context", "color": "#7C3AED"},
    {"from": "memory_manager", "to": "planner", "step": 5, "label": "User data", "color": "#7C3AED"},
    {"from": "planner", "to": "tool_selector", "step": 6, "label": "Intent", "color": "#7C3AED"},
    
    # OpenAPI Registry lookup (NEW)
    {"from": "tool_selector", "to": "openapi_registry", "step": 7, "label": "Load specs", "color": "#7C3AED"},
    {"from": "openapi_registry", "to": "vector_db", "step": 8, "label": "Search ops", "color": "#7C3AED"},
    {"from": "vector_db", "to": "openapi_registry", "step": 9, "label": "Matched", "color": "#7C3AED"},
    {"from": "openapi_registry", "to": "tool_selector", "step": 10, "label": "Tools", "color": "#7C3AED"},
    
    {"from": "tool_selector", "to": "executor", "step": 11, "label": "Tools", "color": "#7C3AED"},
    {"from": "executor", "to": "wealth_agent", "step": 12, "label": "gRPC", "color": "#7C3AED"},
    {"from": "wealth_agent", "to": "azure_openai", "step": 13, "label": "Extract", "color": "#7C3AED"},
    {"from": "azure_openai", "to": "wealth_agent", "step": 14, "label": "account_id", "color": "#7C3AED"},
    
    # OpenAPI Client and validation (NEW)
    {"from": "wealth_agent", "to": "openapi_client", "step": 15, "label": "Call op", "color": "#7C3AED"},
    {"from": "openapi_client", "to": "schema_validator", "step": 16, "label": "Validate", "color": "#7C3AED"},
    {"from": "schema_validator", "to": "openapi_client", "step": 17, "label": "OK", "color": "#7C3AED"},
    {"from": "openapi_client", "to": "accounts_api", "step": 18, "label": "OAuth 2.0", "color": "#7C3AED"},
    {"from": "accounts_api", "to": "openapi_client", "step": 19, "label": "Balance", "color": "#7C3AED"},
    {"from": "openapi_client", "to": "wealth_agent", "step": 20, "label": "Data", "color": "#7C3AED"},
    
    # Response path
    {"from": "wealth_agent", "to": "executor", "step": 21, "label": "Response", "color": "#7C3AED"},
    {"from": "executor", "to": "critic", "step": 22, "label": "Validate", "color": "#7C3AED"},
    {"from": "critic", "to": "governance", "step": 23, "label": "Check", "color": "#7C3AED"},
    {"from": "governance", "to": "critic", "step": 24, "label": "OK", "color": "#7C3AED"},
    {"from": "critic", "to": "planner", "step": 25, "label": "Validated", "color": "#7C3AED"},
    {"from": "planner", "to": "api_gateway", "step": 26, "label": "Response", "color": "#7C3AED"},
    {"from": "api_gateway", "to": "customer", "step": 27, "label": "Response", "color": "#7C3AED"},
]

# New components for OpenAPI flow
OPENAPI_COMPONENTS = {
    "openapi_registry": {
        "id": "openapi_registry",
        "name": "OpenAPI Registry",
        "icon": "📋",
        "layer": "support",
        "color": "#7C3AED",
        "technical": "Stores and searches OpenAPI specifications. Uses vector embeddings to match intents with API operations. Provides semantic search across all available APIs.",
        "layman": "A smart catalog that knows about all available APIs and can find the right one based on what you're trying to do."
    },
    "openapi_client": {
        "id": "openapi_client",
        "name": "OpenAPI Client",
        "icon": "🔌",
        "layer": "support",
        "color": "#7C3AED",
        "technical": "Dynamically generates API clients from OpenAPI specifications. Handles request/response serialization, authentication, and protocol details based on spec.",
        "layman": "A universal connector that can talk to any API by reading its instruction manual (OpenAPI spec)."
    },
    "schema_validator": {
        "id": "schema_validator",
        "name": "Schema Validator",
        "icon": "✅",
        "layer": "support",
        "color": "#7C3AED",
        "technical": "Validates requests and responses against OpenAPI schemas. Ensures data conforms to API contracts before sending and after receiving.",
        "layman": "A quality checker that makes sure we're sending the right information in the right format to APIs."
    }
}

# Enhanced component details for OpenAPI components
OPENAPI_ENHANCED_DETAILS = {
    "openapi_registry": {
        "deployment": "Container (Kubernetes)",
        "deployment_badge": "⭐",
        "deployment_type": "Container (Kubernetes)",
        "protocols": {
            "inbound": "HTTP REST API on port 8080",
            "outbound": "Vector DB query protocol, File system for spec storage"
        },
        "database_operations": [
            "Vector DB: INSERT INTO openapi_specs_embeddings (spec_id, operation_id, embedding)",
            "Vector DB: SELECT * FROM openapi_specs_embeddings WHERE embedding <-> query_embedding < 0.3",
            "File System: READ /specs/{api_name}/openapi.yaml",
            "Redis: HSET openapi:cache:{spec_id} spec '{json_spec}' EX 3600"
        ],
        "functions": [
            "load_spec(api_name) - Loads OpenAPI spec from file system",
            "search_operations(query, top_k=5) - Semantic search for matching operations",
            "get_operation(operation_id) - Retrieves specific operation details",
            "validate_spec(spec) - Validates OpenAPI spec format",
            "embed_operations(spec) - Creates vector embeddings for all operations"
        ],
        "api_calls": [
            "Vector DB: POST /query with embedding vector",
            "Azure OpenAI: POST /embeddings to create operation embeddings"
        ]
    },
    "openapi_client": {
        "deployment": "Container (Kubernetes)",
        "deployment_badge": "⭐",
        "deployment_type": "Container (Kubernetes)",
        "protocols": {
            "inbound": "gRPC on port 50051",
            "outbound": "Dynamic HTTP/HTTPS based on OpenAPI spec"
        },
        "database_operations": [
            "Redis: GET openapi:client:{spec_id} - Cache generated clients",
            "Redis: SETEX openapi:client:{spec_id} 3600 '{client_code}'"
        ],
        "functions": [
            "generate_client(spec) - Dynamically generates API client from spec",
            "call_operation(operation_id, params) - Calls API operation",
            "serialize_request(operation_id, params) - Serializes request based on schema",
            "deserialize_response(operation_id, response) - Deserializes response",
            "handle_auth(spec, credentials) - Handles authentication per spec"
        ],
        "api_calls": [
            "Dynamic: {method} {base_url}{path} based on OpenAPI spec",
            "Example: GET https://api.example.com/accounts/{id}/balance",
            "Auth: OAuth 2.0, API Key, or Bearer token per spec"
        ]
    },
    "schema_validator": {
        "deployment": "Container (Kubernetes)",
        "deployment_badge": "⭐",
        "deployment_type": "Container (Kubernetes)",
        "protocols": {
            "inbound": "gRPC on port 50052",
            "outbound": "None (validation service)"
        },
        "database_operations": [
            "Redis: GET schema:cache:{operation_id} - Cache compiled schemas",
            "Redis: SETEX schema:cache:{operation_id} 3600 '{compiled_schema}'"
        ],
        "functions": [
            "validate_parameters(operation_id, params) - Validates request parameters",
            "validate_response(operation_id, response) - Validates response data",
            "get_schema(operation_id) - Retrieves schema for operation",
            "compile_schema(schema) - Compiles JSON schema for fast validation",
            "format_errors(validation_result) - Formats validation errors"
        ],
        "api_calls": []
    }
}

# Comparison data
FLOW_COMPARISON = {
    "code_based": {
        "name": "Code-Based Flow (Current)",
        "color": "#0066CC",
        "color_name": "Blue",
        "steps": 21,
        "latency_ms": 512,
        "components": 12,
        "external_calls": 2,
        "pros": [
            "Fast - no schema parsing overhead",
            "Type-safe - Python type hints",
            "Simple - fewer components",
            "Reliable - no runtime schema failures",
            "Easy to debug - direct function calls"
        ],
        "cons": [
            "Rigid - requires code changes for new APIs",
            "Tight coupling - hard dependency on API structure",
            "Manual maintenance - update code when APIs change",
            "No self-documentation - need separate API docs",
            "Harder to scale - each new API needs new code"
        ],
        "use_cases": [
            "High-frequency operations (account balance, transactions)",
            "Performance-critical paths",
            "Well-established internal APIs",
            "Production-stable features"
        ]
    },
    "openapi_based": {
        "name": "OpenAPI-Based Flow (Alternative)",
        "color": "#7C3AED",
        "color_name": "Purple",
        "steps": 27,
        "latency_ms": 612,
        "components": 15,
        "external_calls": 3,
        "pros": [
            "Dynamic - add new APIs without code changes",
            "Loose coupling - only depends on OpenAPI specs",
            "Self-documenting - specs serve as documentation",
            "Automatic validation - schema-based validation",
            "Easier to scale - just add new specs",
            "Semantic search - find APIs by description",
            "Versioning - handle multiple API versions"
        ],
        "cons": [
            "Slower - schema parsing overhead (+100ms)",
            "Complex - more components to manage",
            "Runtime errors - schema validation failures",
            "Spec quality - depends on well-written specs",
            "Harder to debug - dynamic code generation"
        ],
        "use_cases": [
            "External partner API integrations",
            "Experimental or beta features",
            "Infrequently used operations",
            "Multi-tenant scenarios with custom APIs"
        ]
    }
}

def get_flow_comparison_summary():
    """Get summary comparison of code-based vs OpenAPI-based flows"""
    return {
        "code_based": FLOW_COMPARISON["code_based"],
        "openapi_based": FLOW_COMPARISON["openapi_based"],
        "difference": {
            "steps": FLOW_COMPARISON["openapi_based"]["steps"] - FLOW_COMPARISON["code_based"]["steps"],
            "latency_ms": FLOW_COMPARISON["openapi_based"]["latency_ms"] - FLOW_COMPARISON["code_based"]["latency_ms"],
            "components": FLOW_COMPARISON["openapi_based"]["components"] - FLOW_COMPARISON["code_based"]["components"],
            "overhead_percentage": round(
                ((FLOW_COMPARISON["openapi_based"]["latency_ms"] - FLOW_COMPARISON["code_based"]["latency_ms"]) 
                 / FLOW_COMPARISON["code_based"]["latency_ms"]) * 100, 1
            )
        }
    }
