# OpenAPI-Based Architecture: System and User Prompts

This document details the exact prompts sent to the LLM when using OpenAPI-based dynamic API discovery and tool selection.

---

## Overview

In the OpenAPI-based architecture, the LLM is used at multiple stages to:
1. **Discover APIs** from OpenAPI Registry
2. **Select appropriate tools** based on user intent
3. **Extract parameters** from user queries
4. **Validate responses** against schemas

Each stage uses specific system and user prompts.

---

## Stage 1: Tool Selector - API Discovery

### System Prompt

```
You are an API discovery assistant for an enterprise banking platform. Your role is to analyze user queries and identify which APIs from the OpenAPI registry are needed to fulfill the request.

**Available API Categories:**
- Account Management (balance, transactions, details)
- Card Services (card details, applications, rewards)
- Loan Services (eligibility, applications, products)
- Wealth Management (investments, portfolio, advice)
- Customer Data (profile, preferences, history)

**Your Task:**
1. Analyze the user's query to understand their intent
2. Identify which API endpoints are needed
3. Return a list of API operation IDs from the OpenAPI registry
4. Consider dependencies (e.g., need customer_id before fetching balance)

**Output Format:**
Return a JSON array of operation IDs:
["operation_id_1", "operation_id_2", ...]

**Guidelines:**
- Only select APIs that are necessary for the query
- Order APIs by dependency (prerequisite APIs first)
- If multiple APIs can fulfill the same need, choose the most efficient one
- Consider data freshness requirements (real-time vs cached)
```

### User Prompt (Example: Account Balance Query)

```
User Query: "What's my account balance?"

Context:
- User ID: user_12345
- Session ID: sess_abc123
- Previous interactions: None
- User location: Dubai, UAE

Available OpenAPI Specs:
- accounts_api_get_balance: GET /api/v1/accounts/{account_id}/balance
- accounts_api_get_transactions: GET /api/v1/accounts/{account_id}/transactions
- accounts_api_get_details: GET /api/v1/accounts/{account_id}/details
- customer_api_get_profile: GET /api/v1/customers/{customer_id}/profile

Identify which API operations are needed to answer this query.
```

### Expected LLM Response

```json
["accounts_api_get_balance"]
```

---

## Stage 2: OpenAPI Registry - Schema Retrieval

### System Prompt

```
You are an OpenAPI schema provider. Given an operation ID, return the complete OpenAPI specification for that operation including:
- HTTP method
- Endpoint path
- Path parameters
- Query parameters
- Request body schema
- Response schema
- Authentication requirements
- Rate limits

Return the schema in OpenAPI 3.0 format.
```

### User Prompt (Example)

```
Operation ID: accounts_api_get_balance

Return the complete OpenAPI specification for this operation.
```

### Expected Response

```yaml
openapi: 3.0.0
paths:
  /api/v1/accounts/{account_id}/balance:
    get:
      operationId: accounts_api_get_balance
      summary: Get account balance
      description: Retrieves the current balance for a customer account
      parameters:
        - name: account_id
          in: path
          required: true
          schema:
            type: string
            pattern: '^ACC[0-9]{10}$'
          description: The unique identifier for the account
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  account_id:
                    type: string
                  balance:
                    type: number
                    format: double
                  currency:
                    type: string
                  as_of_date:
                    type: string
                    format: date-time
      security:
        - OAuth2: [read:accounts]
```

---

## Stage 3: Executor - Parameter Extraction

### System Prompt

```
You are a parameter extraction assistant for API calls. Your role is to extract required parameters from the user's query and context to populate an API request.

**Your Task:**
1. Review the OpenAPI specification for the required parameters
2. Extract parameter values from the user query
3. Extract parameter values from the context (user profile, session data)
4. Validate parameter formats against the schema
5. Return a JSON object with all required parameters

**Guidelines:**
- All required parameters MUST be provided
- Parameter values MUST match the schema type and format
- If a parameter cannot be extracted, return null and set "missing_params": true
- Use context data when available (e.g., user_id from session)
- Apply default values only if specified in the schema
```

### User Prompt (Example)

```
API Operation: accounts_api_get_balance
OpenAPI Spec:
  parameters:
    - name: account_id
      in: path
      required: true
      schema:
        type: string
        pattern: '^ACC[0-9]{10}$'

User Query: "What's my account balance?"

Context:
- User ID: user_12345
- Primary Account ID: ACC0000123456
- Session ID: sess_abc123

Extract all required parameters for this API call.
```

### Expected LLM Response

```json
{
  "account_id": "ACC0000123456",
  "missing_params": false,
  "source": {
    "account_id": "context.primary_account_id"
  }
}
```

---

## Stage 4: OpenAPI Client Generator - Dynamic Client Creation

### System Prompt

```
You are a dynamic API client generator. Given an OpenAPI specification, generate Python code to make the API call using the `requests` library.

**Your Task:**
1. Parse the OpenAPI spec
2. Generate Python code with proper:
   - HTTP method
   - URL construction
   - Headers (including authentication)
   - Request body (if applicable)
   - Error handling
   - Response parsing
3. Include type hints and docstrings

**Output Format:**
Return executable Python code as a string.
```

### User Prompt (Example)

```
OpenAPI Spec:
  GET /api/v1/accounts/{account_id}/balance
  Parameters: account_id (path, required)
  Security: OAuth2
  Response: JSON with balance, currency, as_of_date

Parameters:
  account_id: "ACC0000123456"

OAuth Token: "Bearer eyJhbGc..."

Generate Python code to make this API call.
```

### Expected Response

```python
import requests
from typing import Dict, Any

def call_accounts_api_get_balance(
    account_id: str,
    access_token: str,
    base_url: str = "https://api.bank.com"
) -> Dict[str, Any]:
    """
    Get account balance
    
    Args:
        account_id: The unique identifier for the account
        access_token: OAuth 2.0 access token
        base_url: Base URL for the API
    
    Returns:
        Dict containing balance, currency, and as_of_date
    
    Raises:
        requests.HTTPError: If the API call fails
    """
    url = f"{base_url}/api/v1/accounts/{account_id}/balance"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    return response.json()

# Execute the call
result = call_accounts_api_get_balance(
    account_id="ACC0000123456",
    access_token="eyJhbGc...",
    base_url="https://api.bank.com"
)
```

---

## Stage 5: OpenAPI Validator - Response Validation

### System Prompt

```
You are an API response validator. Your role is to validate API responses against OpenAPI schemas and identify any discrepancies.

**Your Task:**
1. Compare the actual API response with the expected schema
2. Validate data types, formats, and required fields
3. Check for additional fields not in the schema
4. Identify missing required fields
5. Return a validation report

**Output Format:**
```json
{
  "valid": true/false,
  "errors": [...],
  "warnings": [...]
}
```

**Guidelines:**
- Be strict with required fields
- Allow additional fields (open content model)
- Validate format constraints (date-time, email, etc.)
- Check enum values
```

### User Prompt (Example)

```
OpenAPI Response Schema:
  type: object
  required: [account_id, balance, currency, as_of_date]
  properties:
    account_id:
      type: string
    balance:
      type: number
      format: double
    currency:
      type: string
      enum: [USD, EUR, GBP, AED]
    as_of_date:
      type: string
      format: date-time

Actual API Response:
{
  "account_id": "ACC0000123456",
  "balance": 15234.50,
  "currency": "AED",
  "as_of_date": "2024-01-15T10:30:00Z",
  "account_type": "SAVINGS"
}

Validate this response against the schema.
```

### Expected Response

```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    "Additional field 'account_type' not in schema (allowed in open content model)"
  ],
  "summary": {
    "required_fields_present": true,
    "type_validation": "passed",
    "format_validation": "passed",
    "enum_validation": "passed"
  }
}
```

---

## Stage 6: Agent - Response Formatting

### System Prompt

```
You are a customer service assistant for a banking platform. Your role is to format API responses into natural, conversational messages for customers.

**Your Task:**
1. Review the API response data
2. Format it into a friendly, clear message
3. Include relevant details without overwhelming the user
4. Use appropriate formatting (currency, dates, etc.)
5. Add helpful context or next steps if appropriate

**Guidelines:**
- Be conversational and friendly
- Use proper currency formatting
- Format dates in a readable way
- Highlight important information
- Suggest relevant next actions
- Keep messages concise but complete
```

### User Prompt (Example)

```
User Query: "What's my account balance?"

API Response:
{
  "account_id": "ACC0000123456",
  "balance": 15234.50,
  "currency": "AED",
  "as_of_date": "2024-01-15T10:30:00Z",
  "account_type": "SAVINGS"
}

Format this into a conversational response for the customer.
```

### Expected Response

```
Your savings account balance is **AED 15,234.50** as of today at 10:30 AM.

Would you like to:
- View recent transactions
- Transfer funds
- Set up a savings goal
```

---

## Comparison: Code-Based vs OpenAPI-Based Prompts

### Code-Based Architecture
- **No LLM prompts for tool selection** - Uses hardcoded registry
- **Simple parameter extraction** - Direct function calls
- **No schema validation prompts** - Type checking at compile time

### OpenAPI-Based Architecture
- **5 LLM stages** with prompts:
  1. Tool Selector (API discovery)
  2. OpenAPI Registry (schema retrieval)
  3. Executor (parameter extraction)
  4. Client Generator (dynamic code generation)
  5. Validator (response validation)
  6. Agent (response formatting)

---

## Prompt Optimization Strategies

### 1. Few-Shot Learning
Include examples in system prompts:
```
Example 1:
User Query: "Check my balance"
Selected APIs: ["accounts_api_get_balance"]

Example 2:
User Query: "Show me my transactions"
Selected APIs: ["accounts_api_get_transactions"]

Example 3:
User Query: "How much did I spend last month?"
Selected APIs: ["accounts_api_get_transactions", "analytics_api_calculate_spending"]
```

### 2. Chain-of-Thought
Encourage reasoning:
```
Think step-by-step:
1. What is the user asking for?
2. What data is needed to answer?
3. Which APIs provide that data?
4. What are the dependencies?
5. What is the optimal order?
```

### 3. Constraints
Add explicit constraints:
```
Constraints:
- Maximum 3 API calls per query
- Prefer cached data when < 5 minutes old
- Avoid redundant API calls
- Prioritize user-facing APIs over internal APIs
```

---

## Prompt Engineering Best Practices

### 1. Clear Role Definition
- Define the LLM's role explicitly
- Set expectations for output format
- Specify constraints and guidelines

### 2. Structured Output
- Request JSON for machine-readable responses
- Define schema for expected output
- Use consistent field names

### 3. Context Provision
- Include relevant user context
- Provide session information
- Share previous interactions

### 4. Error Handling
- Specify how to handle missing information
- Define fallback behaviors
- Request confidence scores

### 5. Examples
- Include few-shot examples
- Show edge cases
- Demonstrate desired reasoning

---

## Token Usage Estimates

### Per Query (OpenAPI-Based)

| Stage | System Prompt | User Prompt | Response | Total |
|-------|--------------|-------------|----------|-------|
| Tool Selector | 300 tokens | 200 tokens | 50 tokens | 550 tokens |
| Schema Retrieval | 100 tokens | 50 tokens | 400 tokens | 550 tokens |
| Parameter Extraction | 250 tokens | 300 tokens | 100 tokens | 650 tokens |
| Client Generation | 200 tokens | 200 tokens | 300 tokens | 700 tokens |
| Response Validation | 200 tokens | 300 tokens | 150 tokens | 650 tokens |
| Response Formatting | 250 tokens | 200 tokens | 100 tokens | 550 tokens |
| **Total** | | | | **3,650 tokens** |

### Cost Comparison (GPT-4)

- **Code-Based**: ~500 tokens per query ($0.015)
- **OpenAPI-Based**: ~3,650 tokens per query ($0.11)
- **Cost Increase**: 7.3x

---

## Summary

The OpenAPI-based architecture uses **6 distinct LLM stages** with carefully crafted prompts to enable dynamic API discovery and tool selection. While this provides flexibility and adaptability, it comes with increased latency (+100ms) and cost (7.3x) compared to the code-based approach.

**Key Takeaways:**
- System prompts define role and output format
- User prompts provide context and specific requests
- Structured outputs (JSON) enable machine processing
- Few-shot examples improve accuracy
- Chain-of-thought reasoning enhances reliability
- Token usage is significantly higher than code-based approach
