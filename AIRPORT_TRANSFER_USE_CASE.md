# Airport Transfer Booking Use Case Analysis

## Overview

This use case demonstrates a complete chatbot journey for booking an airport transfer, including proactive engagement, travel card updates, and points redemption upsells.

---

## User Journey Summary

**Scenario**: Customer has booked a flight. The chatbot proactively offers airport transfer booking, then cross-sells travel card updates and points redemption.

**Steps**: 22 steps from initial engagement to points redemption offer

**Duration**: ~5-7 minutes

**Outcome**: Airport transfer booked, card enabled for international use, points redemption offered

---

## Components Involved

### 1. Entry Layer
- **Customer** (Mobile/Voice & IVR) - Initiates interaction via banking app
- **Authentication** - Validates user session (already logged in)
- **API Gateway** - Routes chatbot requests

### 2. Security Layer
- **WAF** - Protects chatbot endpoints
- **Rate Limiter** - Prevents abuse
- **Content Filter** - Validates user inputs

### 3. Orchestration Layer
- **Planner** - Understands intent (airport transfer, travel update, points redemption)
- **Tool Selector** - Identifies needed tools (flight API, card API, CRM, rewards API)
- **Executor** - Coordinates agent execution
- **Critic** - Validates responses

### 4. Agent Layer
- **Card Agent** - Handles travel card update
- **Wealth Agent** - Manages Vantage points and Skywards Miles conversion

### 5. Support Services
- **MCP Tools** - Integrates with external APIs
- **RAG Engine** - Retrieves card benefits information
- **Memory Manager** - Stores conversation context and user preferences
- **Context Manager** - Maintains conversation state across steps

### 6. Data Layer
- **Cosmos DB** - Stores conversation history and booking details
- **Redis** - Caches user profile and card information
- **Vector DB** - Stores card benefits and travel information

### 7. External Services (via MCP Tools)
- **Cards API** - Enables/disables international card usage
- **CRM (Salesforce)** - Retrieves customer profile and flight booking
- **Flight Booking System** - Fetches flight details (Emirates integration)
- **Airport Transfer Service** - Books ride (3rd party API)
- **Rewards API** - Checks Vantage points balance and converts to Skywards Miles

### 8. Governance Layer
- **LLM Governance** - Validates chatbot responses for compliance
- **Audit Service** - Logs all transactions
- **Token Cost Governance** - Tracks API usage

### 9. Messaging Layer (Kafka)
- **Kafka Broker** - Publishes booking events
- **Analytics Service** - Tracks conversion metrics
- **Audit Service** - Records compliance trail

### 10. Observability
- **Monitoring** - Tracks chatbot performance and errors

---

## Detailed Flow (22 Steps)

### Phase 1: Proactive Engagement (Steps 1-3)

**Step 1: Home Screen**
- User views banking app home screen
- Chatbot widget visible with quick actions
- **Components**: Customer → API Gateway → Planner

**Step 2: Proactive Message**
- Chatbot detects flight booking in CRM
- Sends proactive message: "I see you've booked a flight..."
- **Components**: Planner → Memory Manager (retrieve context) → CRM (via MCP Tools) → RAG Engine (card benefits)

**Step 3: Benefits Display**
- Shows Solitaire Card benefits list
- Offers free airport transfer
- **Components**: RAG Engine → Vector DB → Planner

### Phase 2: Airport Transfer Booking (Steps 4-11)

**Step 4: User Clicks "Book an airport transfer"**
- **Components**: Customer → API Gateway → Planner → Tool Selector

**Step 5: Flight Details Request**
- Chatbot asks: "May I have your flight reference and travel dates?"
- **Components**: Planner → Executor

**Step 6: User Provides Flight Info**
- User responds: "FZDKWE Nov 10-Feb 15"
- **Components**: Customer → API Gateway → Planner → Memory Manager (store)

**Step 7: Processing Details**
- Retrieves home address from profile
- Calculates pickup time (3 hours before check-in)
- **Components**: Planner → CRM (via MCP Tools) → Flight API (via MCP Tools)

**Step 8: Booking Summary Display**
- Shows Emirates-branded card with flight and transfer details
- **Components**: Executor → Planner

**Step 9: Confirm or Edit Options**
- Presents two buttons: Confirm / Edit
- **Components**: Planner

**Step 10: User Confirms**
- User clicks "Confirm booking"
- **Components**: Customer → API Gateway → Executor

**Step 11: Booking Confirmed**
- Calls Airport Transfer API to book ride
- Stores booking in Cosmos DB
- Sends confirmation message
- Publishes event to Kafka
- **Components**: Executor → MCP Tools → Airport Transfer API → Cosmos DB → Kafka → Audit Service

### Phase 3: Travel Card Update (Steps 12-18)

**Step 12: Cross-Sell Offer**
- Chatbot offers: "Would you like to select a card for a travel update?"
- **Components**: Planner (cross-sell logic) → Card Agent

**Step 13: User Chooses "Yes"**
- Two options presented: Travel update / Travel insurance
- **Components**: Customer → API Gateway → Card Agent

**Step 14: Single Action Button**
- Shows only "Yes, do a travel update"
- **Components**: Card Agent

**Step 15: Card Selection Prompt**
- Asks: "Select a card for a travel update:"
- **Components**: Card Agent → Cards API (via MCP Tools) - retrieve user cards

**Step 16: Card Display**
- Shows Solitaire Credit Card with balance
- **Components**: Card Agent → Redis (cached card data)

**Step 17: User Selects Card**
- User clicks "Solitaire Credit Card"
- **Components**: Customer → API Gateway → Card Agent

**Step 18: Travel Update Confirmed**
- Calls Cards API to enable international use
- Stores update in Cosmos DB
- Confirmation: "Your card is now set for international use"
- **Components**: Card Agent → MCP Tools → Cards API → Cosmos DB → Governance → Kafka

### Phase 4: Points Redemption Upsell (Steps 19-22)

**Step 19: Vantage Points Promotion**
- Retrieves points balance from Rewards API
- Offers: "You have 120,345,678 Vantage points! Convert to Skywards Miles"
- **Components**: Planner → Wealth Agent → MCP Tools → Rewards API

**Step 20: Specific Redemption Offer**
- Suggests: "Redeem 135,000 points towards Skywards Miles?"
- **Components**: Wealth Agent → RAG Engine (conversion rates)

**Step 21: User Choice**
- Presents: "Yes, redeem" / "No, don't redeem"
- **Components**: Wealth Agent

**Step 22: Awaiting Confirmation**
- If Yes: Calls Rewards API to convert points
- If No: Ends conversation gracefully
- **Components**: Wealth Agent → MCP Tools → Rewards API → Cosmos DB → Kafka

---

## Data Flow

### Request Path (Forward)

```
Customer (Mobile App)
  → API Gateway (HTTPS/REST)
  → Authentication (JWT validation)
  → Security Layer (WAF, Rate Limiter, Content Filter)
  → Planner (intent classification)
  → Memory Manager (retrieve context)
  → Tool Selector (identify tools: CRM, Flight API, Cards API, Rewards API)
  → Executor (route to agents)
  → Card Agent / Wealth Agent
  → Azure OpenAI (generate responses)
  → MCP Tools (call external APIs)
  → External APIs (CRM, Flight, Cards, Airport Transfer, Rewards)
  → Cosmos DB (store transactions)
  → Kafka (publish events)
  → Governance (validate compliance)
```

### Response Path (Backward)

```
External APIs (return data)
  → MCP Tools (format response)
  → Card Agent / Wealth Agent (process data)
  → Azure OpenAI (generate natural language)
  → Executor (validate)
  → Critic (check quality)
  → Planner (finalize response)
  → API Gateway (format for mobile)
  → Customer (display in chatbot)
```

---

## External API Calls

### 1. CRM (Salesforce) - via MCP Tools
- **Purpose**: Retrieve customer profile and flight booking
- **Endpoint**: GET /services/data/v58.0/query
- **Query**: `SELECT FlightReference, TravelDates, HomeAddress FROM Customer WHERE UserId = '{user_id}'`
- **Response**: Flight booking details

### 2. Flight Booking System (Emirates API) - via MCP Tools
- **Purpose**: Get flight details and calculate check-in time
- **Endpoint**: GET /api/v1/flights/{flight_reference}
- **Response**: Flight time, terminal, check-in time

### 3. Airport Transfer Service - via MCP Tools
- **Purpose**: Book ride from home to airport
- **Endpoint**: POST /api/v1/bookings
- **Payload**: 
```json
{
  "pickup_address": "123 Boulevard, Downtown, Dubai",
  "dropoff_address": "DXB Int. Airport, Terminal 3",
  "pickup_time": "2025-10-20T17:00:00Z",
  "passenger_name": "...",
  "flight_reference": "FZDKWE"
}
```
- **Response**: Booking confirmation ID

### 4. Cards API - via MCP Tools
- **Purpose**: Enable international card usage
- **Endpoint**: PUT /api/v1/cards/{card_id}/international
- **Payload**:
```json
{
  "enabled": true,
  "start_date": "2024-11-10",
  "end_date": "2025-02-15",
  "reason": "travel"
}
```
- **Response**: Card update confirmation

### 5. Rewards API - via MCP Tools
- **Purpose**: Check balance and convert points
- **Endpoints**:
  - GET /api/v1/rewards/balance?user_id={user_id}
  - POST /api/v1/rewards/convert
- **Payload** (convert):
```json
{
  "from_program": "Vantage",
  "to_program": "Skywards",
  "points": 135000,
  "user_id": "..."
}
```
- **Response**: Conversion confirmation

---

## Database Operations

### Cosmos DB (MongoDB)
```javascript
// Store airport transfer booking
bookings.insertOne({
  booking_id: "ATB-2024-001",
  user_id: "user123",
  type: "airport_transfer",
  flight_reference: "FZDKWE",
  pickup_time: "2025-10-20T17:00:00Z",
  pickup_address: "123 Boulevard, Downtown, Dubai",
  dropoff_address: "DXB Int. Airport, Terminal 3",
  status: "confirmed",
  created_at: new Date()
})

// Store travel card update
card_updates.insertOne({
  update_id: "CU-2024-001",
  user_id: "user123",
  card_id: "card_solitaire_1234",
  international_enabled: true,
  start_date: "2024-11-10",
  end_date: "2025-02-15",
  created_at: new Date()
})

// Store conversation history
conversations.insertOne({
  conversation_id: "conv_2024_001",
  user_id: "user123",
  messages: [...],
  context: {
    flight_reference: "FZDKWE",
    travel_dates: "Nov 10 - Feb 15",
    booking_confirmed: true,
    card_updated: true
  },
  created_at: new Date()
})
```

### Redis (Caching)
```redis
# Cache user profile
HSET user:user123 name "John Doe" home_address "123 Boulevard, Downtown, Dubai"
EXPIRE user:user123 3600

# Cache card details
HSET card:solitaire_1234 balance "15230.00" last_four "1234" type "Solitaire"
EXPIRE card:solitaire_1234 1800

# Cache Vantage points
SET rewards:user123:vantage 120345678 EX 1800
```

### Vector DB (RAG)
```
# Query card benefits
query = "Solitaire Card travel benefits"
results = vector_db.similarity_search(query, top_k=10)
# Returns: Lounge access, travel insurance, cashback, etc.
```

---

## Kafka Events

### Topic: agent.executions
```json
{
  "event_id": "evt_001",
  "agent": "card_agent",
  "action": "enable_international_card",
  "user_id": "user123",
  "card_id": "card_solitaire_1234",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "success"
}
```

### Topic: external.crm.events
```json
{
  "event_id": "evt_002",
  "source": "airport_transfer_service",
  "type": "booking_confirmed",
  "booking_id": "ATB-2024-001",
  "user_id": "user123",
  "timestamp": "2024-01-15T10:25:00Z"
}
```

---

## Performance Metrics

### Latency Breakdown
- **Step 2 (Proactive Message)**: ~300ms (CRM query + RAG retrieval)
- **Step 7 (Processing Details)**: ~500ms (CRM + Flight API + calculation)
- **Step 11 (Booking Confirmed)**: ~800ms (Airport Transfer API + DB write + Kafka publish)
- **Step 18 (Travel Update Confirmed)**: ~400ms (Cards API + DB write)
- **Step 19 (Points Balance)**: ~200ms (Rewards API query)

**Total Journey Time**: ~2.2 seconds (API calls only, excluding user interaction time)

### API Call Count
- **CRM**: 2 calls (profile + flight booking)
- **Flight API**: 1 call (flight details)
- **Airport Transfer API**: 1 call (booking)
- **Cards API**: 2 calls (list cards + enable international)
- **Rewards API**: 1 call (balance check)

**Total**: 7 external API calls

---

## Business Value

### Primary Outcome
- ✅ Airport transfer booked (revenue: ~$50-100)
- ✅ Card enabled for international use (reduced fraud calls)
- ✅ Points redemption offered (increased engagement)

### Secondary Benefits
- **Customer Satisfaction**: Proactive service, seamless experience
- **Cross-Sell Success**: 2 additional services offered after initial booking
- **Operational Efficiency**: Automated booking vs. call center
- **Data Collection**: Travel preferences, spending patterns

### Conversion Metrics
- **Airport Transfer Conversion**: ~40% (from proactive offer)
- **Travel Card Update**: ~70% (from transfer booking)
- **Points Redemption**: ~25% (from card update)

---

## Summary

**This use case demonstrates:**

1. **Proactive Engagement**: Chatbot detects flight booking and offers relevant service
2. **Multi-Agent Coordination**: Card Agent and Wealth Agent work together
3. **External API Integration**: 5 different external systems via MCP Tools
4. **Cross-Sell Strategy**: 3 services offered in sequence (transfer → card → points)
5. **Complete Data Flow**: From customer request through all layers to external APIs and back
6. **Event-Driven Architecture**: Kafka events for analytics and audit
7. **Governance & Compliance**: All transactions logged and validated

**Components Used**: 26 out of 34 total components (76% of architecture)

**Flow Complexity**: High - involves orchestration, multiple agents, external APIs, database operations, and event streaming
