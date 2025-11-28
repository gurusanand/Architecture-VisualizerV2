"""
Airport Transfer Booking Use Case Flow Definition
Complete 22-step journey with all components
"""

AIRPORT_TRANSFER_FLOW = {
    "name": "Airport Transfer Booking Journey",
    "description": "Complete chatbot journey: Proactive engagement → Airport transfer booking → Travel card update → Points redemption",
    "duration": "~5-7 minutes",
    "api_calls": 7,
    "total_latency": "2200ms",
    "components_used": 26,
    "phases": [
        {
            "id": 1,
            "name": "Proactive Engagement",
            "steps": [1, 2, 3],
            "description": "Chatbot detects flight booking and offers airport transfer"
        },
        {
            "id": 2,
            "name": "Airport Transfer Booking",
            "steps": [4, 5, 6, 7, 8, 9, 10, 11],
            "description": "User books airport transfer with flight details"
        },
        {
            "id": 3,
            "name": "Travel Card Update",
            "steps": [12, 13, 14, 15, 16, 17, 18],
            "description": "Enable card for international use during travel"
        },
        {
            "id": 4,
            "name": "Points Redemption Upsell",
            "steps": [19, 20, 21, 22],
            "description": "Offer to convert Vantage points to Skywards Miles"
        }
    ],
    "steps": [
        {
            "id": 1,
            "phase": "Proactive Engagement",
            "title": "Home Screen - Initial State",
            "user_action": "Views banking app home screen",
            "chatbot_action": "Displays widget with quick actions",
            "components": ["customer", "api_gateway", "planner"],
            "protocol": "HTTPS/REST",
            "latency": "50ms"
        },
        {
            "id": 2,
            "phase": "Proactive Engagement",
            "title": "Chatbot Proactive Engagement",
            "user_action": "None (proactive)",
            "chatbot_action": "Detects flight booking, sends proactive message",
            "components": ["planner", "memory_manager", "mcp_tools", "crm", "rag_engine", "vector_db"],
            "protocol": "gRPC + HTTPS/REST + OAuth 2.0",
            "latency": "300ms",
            "api_call": "CRM: GET /services/data/v58.0/query (flight booking)"
        },
        {
            "id": 3,
            "phase": "Proactive Engagement",
            "title": "Benefits Display",
            "user_action": "Reads Solitaire Card benefits",
            "chatbot_action": "Shows 10 card benefits, offers free airport transfer",
            "components": ["rag_engine", "vector_db", "planner"],
            "protocol": "Internal",
            "latency": "100ms"
        },
        {
            "id": 4,
            "phase": "Airport Transfer Booking",
            "title": "User Clicks 'Book an airport transfer'",
            "user_action": "Clicks button",
            "chatbot_action": "Initiates booking flow",
            "components": ["customer", "api_gateway", "planner", "tool_selector"],
            "protocol": "HTTPS/REST",
            "latency": "50ms"
        },
        {
            "id": 5,
            "phase": "Airport Transfer Booking",
            "title": "Flight Details Request",
            "user_action": "None",
            "chatbot_action": "Asks for flight reference and travel dates",
            "components": ["planner", "executor"],
            "protocol": "Internal",
            "latency": "30ms"
        },
        {
            "id": 6,
            "phase": "Airport Transfer Booking",
            "title": "User Provides Flight Info",
            "user_action": "Types 'FZDKWE Nov 10-Feb 15'",
            "chatbot_action": "Stores flight info in memory",
            "components": ["customer", "api_gateway", "planner", "memory_manager", "redis"],
            "protocol": "HTTPS/REST + Redis",
            "latency": "80ms"
        },
        {
            "id": 7,
            "phase": "Airport Transfer Booking",
            "title": "Processing Details",
            "user_action": "None",
            "chatbot_action": "Retrieves address, gets flight details, calculates pickup time",
            "components": ["planner", "mcp_tools", "crm", "executor", "azure_openai"],
            "protocol": "gRPC + HTTPS/REST + OAuth 2.0",
            "latency": "500ms",
            "api_call": "CRM: GET customer profile, Flight API: GET flight details"
        },
        {
            "id": 8,
            "phase": "Airport Transfer Booking",
            "title": "Booking Summary Display",
            "user_action": "Reviews booking details",
            "chatbot_action": "Shows Emirates-branded card with all details",
            "components": ["executor", "planner"],
            "protocol": "Internal",
            "latency": "50ms"
        },
        {
            "id": 9,
            "phase": "Airport Transfer Booking",
            "title": "Confirm or Edit Options",
            "user_action": "Sees two buttons",
            "chatbot_action": "Presents Confirm / Edit options",
            "components": ["planner"],
            "protocol": "Internal",
            "latency": "20ms"
        },
        {
            "id": 10,
            "phase": "Airport Transfer Booking",
            "title": "User Confirms Booking",
            "user_action": "Clicks 'Confirm booking'",
            "chatbot_action": "Initiates API call to book transfer",
            "components": ["customer", "api_gateway", "executor"],
            "protocol": "HTTPS/REST",
            "latency": "50ms"
        },
        {
            "id": 11,
            "phase": "Airport Transfer Booking",
            "title": "Booking Confirmed",
            "user_action": "Reads confirmation",
            "chatbot_action": "Books transfer, stores in DB, publishes event, sends confirmation",
            "components": ["executor", "mcp_tools", "cosmos_db", "kafka", "audit_service", "governance"],
            "protocol": "HTTPS/REST + OAuth 2.0 + Kafka",
            "latency": "800ms",
            "api_call": "Airport Transfer API: POST /api/v1/bookings"
        },
        {
            "id": 12,
            "phase": "Travel Card Update",
            "title": "Cross-Sell Offer",
            "user_action": "Reads offer",
            "chatbot_action": "Offers travel card update service",
            "components": ["planner", "card_agent"],
            "protocol": "gRPC",
            "latency": "50ms"
        },
        {
            "id": 13,
            "phase": "Travel Card Update",
            "title": "User Chooses 'Yes'",
            "user_action": "Sees two options: Travel update / Insurance",
            "chatbot_action": "Presents choice",
            "components": ["customer", "api_gateway", "card_agent"],
            "protocol": "HTTPS/REST + gRPC",
            "latency": "40ms"
        },
        {
            "id": 14,
            "phase": "Travel Card Update",
            "title": "Single Action Button",
            "user_action": "Sees 'Yes, do a travel update' button",
            "chatbot_action": "Streamlines to single option",
            "components": ["card_agent"],
            "protocol": "Internal",
            "latency": "20ms"
        },
        {
            "id": 15,
            "phase": "Travel Card Update",
            "title": "Card Selection Prompt",
            "user_action": "Reads prompt",
            "chatbot_action": "Asks to select a card, retrieves user's cards",
            "components": ["card_agent", "mcp_tools", "cards_api", "redis"],
            "protocol": "HTTPS/REST + OAuth 2.0 + Redis",
            "latency": "200ms",
            "api_call": "Cards API: GET /api/v1/cards?user_id={id}"
        },
        {
            "id": 16,
            "phase": "Travel Card Update",
            "title": "Card Display",
            "user_action": "Sees Solitaire Credit Card details",
            "chatbot_action": "Shows card with balance and last 4 digits",
            "components": ["card_agent", "redis"],
            "protocol": "Redis",
            "latency": "30ms"
        },
        {
            "id": 17,
            "phase": "Travel Card Update",
            "title": "User Selects Card",
            "user_action": "Clicks 'Solitaire Credit Card'",
            "chatbot_action": "Initiates card update",
            "components": ["customer", "api_gateway", "card_agent"],
            "protocol": "HTTPS/REST + gRPC",
            "latency": "50ms"
        },
        {
            "id": 18,
            "phase": "Travel Card Update",
            "title": "Travel Update Confirmed",
            "user_action": "Reads confirmation",
            "chatbot_action": "Enables international use, stores update, publishes event",
            "components": ["card_agent", "mcp_tools", "cards_api", "cosmos_db", "governance", "kafka"],
            "protocol": "HTTPS/REST + OAuth 2.0 + Kafka",
            "latency": "400ms",
            "api_call": "Cards API: PUT /api/v1/cards/{id}/international"
        },
        {
            "id": 19,
            "phase": "Points Redemption Upsell",
            "title": "Vantage Points Promotion",
            "user_action": "Reads points balance",
            "chatbot_action": "Retrieves points balance, offers conversion to Skywards Miles",
            "components": ["planner", "wealth_agent", "mcp_tools", "azure_openai"],
            "protocol": "gRPC + HTTPS/REST + OAuth 2.0",
            "latency": "200ms",
            "api_call": "Rewards API: GET /api/v1/rewards/balance"
        },
        {
            "id": 20,
            "phase": "Points Redemption Upsell",
            "title": "Specific Redemption Offer",
            "user_action": "Reads offer",
            "chatbot_action": "Suggests redeeming 135,000 points",
            "components": ["wealth_agent", "rag_engine"],
            "protocol": "Internal",
            "latency": "80ms"
        },
        {
            "id": 21,
            "phase": "Points Redemption Upsell",
            "title": "User Choice",
            "user_action": "Sees 'Yes, redeem' / 'No, don't redeem' buttons",
            "chatbot_action": "Presents choice",
            "components": ["wealth_agent"],
            "protocol": "Internal",
            "latency": "20ms"
        },
        {
            "id": 22,
            "phase": "Points Redemption Upsell",
            "title": "Awaiting Confirmation",
            "user_action": "Can click Yes or No",
            "chatbot_action": "If Yes: converts points; If No: ends gracefully",
            "components": ["wealth_agent", "mcp_tools", "cosmos_db", "kafka"],
            "protocol": "HTTPS/REST + OAuth 2.0 + Kafka",
            "latency": "300ms (if Yes)",
            "api_call": "Rewards API: POST /api/v1/rewards/convert (if Yes)"
        }
    ],
    "component_list": [
        "customer",
        "api_gateway",
        "authentication",
        "waf",
        "rate_limiter",
        "content_filter",
        "planner",
        "tool_selector",
        "executor",
        "critic",
        "card_agent",
        "wealth_agent",
        "mcp_tools",
        "rag_engine",
        "memory_manager",
        "context_manager",
        "cosmos_db",
        "redis",
        "vector_db",
        "cards_api",
        "crm",
        "azure_openai",
        "governance",
        "kafka",
        "analytics_service",
        "audit_service"
    ],
    "api_calls_summary": [
        {"step": 2, "api": "CRM (Salesforce)", "method": "GET", "endpoint": "/services/data/v58.0/query", "purpose": "Retrieve flight booking"},
        {"step": 7, "api": "CRM (Salesforce)", "method": "GET", "endpoint": "/services/data/v58.0/query", "purpose": "Get customer profile and address"},
        {"step": 7, "api": "Flight Booking System", "method": "GET", "endpoint": "/api/v1/flights/{ref}", "purpose": "Get flight details"},
        {"step": 11, "api": "Airport Transfer Service", "method": "POST", "endpoint": "/api/v1/bookings", "purpose": "Book airport transfer"},
        {"step": 15, "api": "Cards API", "method": "GET", "endpoint": "/api/v1/cards", "purpose": "List user's cards"},
        {"step": 18, "api": "Cards API", "method": "PUT", "endpoint": "/api/v1/cards/{id}/international", "purpose": "Enable international use"},
        {"step": 19, "api": "Rewards API", "method": "GET", "endpoint": "/api/v1/rewards/balance", "purpose": "Get Vantage points balance"},
        {"step": 22, "api": "Rewards API", "method": "POST", "endpoint": "/api/v1/rewards/convert", "purpose": "Convert points to Skywards Miles"}
    ],
    "database_operations": [
        {"step": 6, "db": "Redis", "operation": "HSET", "purpose": "Cache flight info"},
        {"step": 11, "db": "Cosmos DB", "operation": "insertOne", "collection": "bookings", "purpose": "Store airport transfer booking"},
        {"step": 11, "db": "Cosmos DB", "operation": "insertOne", "collection": "conversations", "purpose": "Store conversation history"},
        {"step": 16, "db": "Redis", "operation": "HGET", "purpose": "Retrieve cached card details"},
        {"step": 18, "db": "Cosmos DB", "operation": "insertOne", "collection": "card_updates", "purpose": "Store card update"},
        {"step": 22, "db": "Cosmos DB", "operation": "insertOne", "collection": "rewards_transactions", "purpose": "Store points conversion"}
    ],
    "kafka_events": [
        {"step": 11, "topic": "agent.executions", "purpose": "Log booking execution"},
        {"step": 11, "topic": "external.crm.events", "purpose": "Publish booking event"},
        {"step": 18, "topic": "agent.executions", "purpose": "Log card update execution"},
        {"step": 22, "topic": "agent.executions", "purpose": "Log points conversion execution"}
    ],
    "business_metrics": {
        "conversion_rates": {
            "airport_transfer": "40%",
            "travel_card_update": "70%",
            "points_redemption": "25%"
        },
        "revenue": {
            "airport_transfer": "$50-100",
            "points_conversion_value": "$1,350"
        },
        "customer_satisfaction": "High - proactive, seamless experience",
        "operational_efficiency": "Automated vs. call center"
    }
}
