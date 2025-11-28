# RAG Engine vs API Calls - When to Use What

## 🎯 Key Principle

**RAG Engine** = Static Knowledge (Policies, Products, FAQs)  
**API Calls** = Real-Time Data (Balances, Transactions, Applications)

---

## ✅ Use RAG Engine For:

### 1. **Static Knowledge Base**
- Company policies
- Product catalogs
- FAQ answers
- Business hours
- Branch locations
- Interest rates (published rates, not personalized)
- Loan products available
- Credit card features
- Investment product descriptions

### 2. **Historical Information**
- Past announcements
- Archived documents
- Training materials
- Compliance guidelines

### 3. **General Queries**
Examples:
- "What are your business hours?"
- "What credit cards do you offer?"
- "What is your privacy policy?"
- "Where is the nearest branch?"
- "What are the features of your premium savings account?"

### Flow:
```
Planner → RAG Engine → Azure OpenAI (format) → Critic → Customer
```

**No agent needed, no API call needed**

---

## ✅ Use API Calls (via MCP Tools) For:

### 1. **Real-Time Account Data**
- Current account balance
- Recent transactions
- Available credit
- Pending transactions
- Account status
- Card activation status

### 2. **Personalized Information**
- Customer-specific loan eligibility
- Personalized interest rates
- Credit score
- Reward points balance
- Account history

### 3. **Transactional Operations**
- Create card application
- Submit loan application
- Update account settings
- Create CRM case
- Transfer funds

### Examples:
- "What is my account balance?" → **Accounts API**
- "What are my recent transactions?" → **Accounts API**
- "What is my credit card balance?" → **Cards API**
- "Am I eligible for a home loan?" → **Loans API**
- "How many reward points do I have?" → **Cards API**
- "Apply for a new credit card" → **Cards API + CRM**

### Flow:
```
Planner → Tool Selector → Executor → Domain Agent → Azure OpenAI (understand)
  → Domain Agent → MCP Tools → Domain API → Backend System
  → Response back through same path
```

**Agent needed, API call required**

---

## 🔄 Use BOTH For:

### Complex Queries Requiring Both Static and Dynamic Data

#### Example 1: Investment Advice
**Query**: "Should I invest in stocks or bonds given my age and risk tolerance?"

**Needs:**
1. **API Call**: Current account balance (real-time) → **Accounts API**
2. **RAG**: Investment product catalog (static) → **RAG Engine**
3. **Memory**: User's age and risk profile (stored context) → **Memory Manager**

**Flow:**
```
Wealth Agent → MCP Tools → Accounts API (get balance)
  → Wealth Agent → RAG Engine (get investment products)
  → Wealth Agent combines: balance + products + risk profile
  → Returns personalized recommendation
```

#### Example 2: Loan Recommendation
**Query**: "What loan options do I have based on my income?"

**Needs:**
1. **API Call**: Loan eligibility check (personalized) → **Loans API**
2. **RAG**: Available loan products (catalog) → **RAG Engine**
3. **Memory**: User's income and employment (stored context) → **Memory Manager**

**Flow:**
```
Loan Agent → MCP Tools → Loans API (check eligibility)
  → Loan Agent → RAG Engine (get loan products)
  → Loan Agent filters products based on eligibility
  → Returns personalized loan options
```

#### Example 3: Card Recommendation
**Query**: "Which credit card is best for me?"

**Needs:**
1. **API Call**: Credit score and spending patterns (personalized) → **CRM API**
2. **RAG**: Credit card features and benefits (catalog) → **RAG Engine**
3. **Memory**: User's spending habits (stored context) → **Memory Manager**

**Flow:**
```
Card Agent → MCP Tools → CRM API (get credit score)
  → Card Agent → RAG Engine (get card catalog)
  → Card Agent matches cards to credit score and spending
  → Returns personalized card recommendations
```

---

## 📊 Decision Matrix

| Query Type | Example | Use RAG? | Use API? | Use Agent? |
|------------|---------|----------|----------|------------|
| **Static Info** | "What are your business hours?" | ✅ Yes | ❌ No | ❌ No |
| **Product Catalog** | "What credit cards do you offer?" | ✅ Yes | ❌ No | ❌ No |
| **Real-Time Balance** | "What is my account balance?" | ❌ No | ✅ Yes | ✅ Yes |
| **Transaction History** | "Show my last 10 transactions" | ❌ No | ✅ Yes | ✅ Yes |
| **Eligibility Check** | "Am I eligible for a loan?" | ❌ No | ✅ Yes | ✅ Yes |
| **Application** | "Apply for a credit card" | ❌ No | ✅ Yes | ✅ Yes |
| **Personalized Advice** | "Best investment for me?" | ✅ Yes | ✅ Yes | ✅ Yes |
| **Product + Eligibility** | "Which loans can I get?" | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🚫 Common Mistakes

### ❌ WRONG: Using RAG for Real-Time Data
```
Query: "What is my account balance?"
Wrong Flow: Planner → RAG Engine → Response

Problem: RAG doesn't have real-time balance data!
```

### ✅ CORRECT: Using API for Real-Time Data
```
Query: "What is my account balance?"
Correct Flow: Planner → Tool Selector → Executor → Wealth Agent 
  → MCP Tools → Accounts API → Real-time balance
```

---

### ❌ WRONG: Using API for Static Knowledge
```
Query: "What are your business hours?"
Wrong Flow: Planner → Executor → Agent → MCP Tools → API

Problem: Unnecessary complexity and API calls for static data!
```

### ✅ CORRECT: Using RAG for Static Knowledge
```
Query: "What are your business hours?"
Correct Flow: Planner → RAG Engine → Response

Benefit: Fast, no API overhead, no agent needed
```

---

## 🎓 Sample Queries with Correct Routing

### 1. Bank Balance Check
**Query**: "I want to check my bank balance"

**Routing Decision:**
- Real-time data needed? **YES** → Use API
- Static knowledge needed? **NO**
- Agent needed? **YES** (Wealth Agent)

**Flow:**
```
Customer → API Gateway → Planner → Tool Selector → Executor
  → Wealth Agent → MCP Tools → Accounts API
  → Accounts API → Core Banking (real-time balance)
  → Response back to customer
```

**NO RAG ENGINE** - Direct API call for real-time data

---

### 2. Investment Advice
**Query**: "Should I invest in stocks or bonds?"

**Routing Decision:**
- Real-time data needed? **YES** (current balance) → Use API
- Static knowledge needed? **YES** (investment products) → Use RAG
- Agent needed? **YES** (Wealth Agent)

**Flow:**
```
Customer → API Gateway → Planner → Tool Selector → Executor
  → Wealth Agent → MCP Tools → Accounts API (balance)
  → Wealth Agent → RAG Engine (investment products)
  → Wealth Agent combines data → Response to customer
```

**BOTH API AND RAG** - API for balance, RAG for products

---

### 3. General Question
**Query**: "What are your business hours?"

**Routing Decision:**
- Real-time data needed? **NO**
- Static knowledge needed? **YES** → Use RAG
- Agent needed? **NO**

**Flow:**
```
Customer → API Gateway → Planner → RAG Engine
  → Azure OpenAI (format) → Response to customer
```

**ONLY RAG** - No agent, no API, just knowledge base

---

### 4. Card Application
**Query**: "I want to apply for a new credit card"

**Routing Decision:**
- Real-time data needed? **YES** (create application) → Use API
- Static knowledge needed? **NO** (or minimal)
- Agent needed? **YES** (Card Agent)

**Flow:**
```
Customer → API Gateway → Planner → Tool Selector → Executor
  → Card Agent → MCP Tools → Cards API (create application)
  → Card Agent → MCP Tools → CRM (create case)
  → Response to customer
```

**API CALLS** - Two APIs (Cards API + CRM), no RAG needed

---

## 📝 Summary

### RAG Engine = Knowledge Base
- **What it has**: Policies, products, FAQs, static information
- **When to use**: General questions, product catalogs, company info
- **Speed**: Fast (no external API calls)
- **Data freshness**: Updated periodically (not real-time)

### API Calls = Live Data
- **What it has**: Real-time balances, transactions, personalized data
- **When to use**: Account queries, applications, personalized info
- **Speed**: Slower (external API latency)
- **Data freshness**: Real-time (current data)

### Best Practice
1. **Analyze the query intent**
2. **Determine data source needed**:
   - Static knowledge? → RAG
   - Real-time data? → API
   - Both? → Use both
3. **Route accordingly**:
   - Simple static query → Direct to RAG (no agent)
   - Real-time query → Route to Agent → MCP Tools → API
   - Complex query → Route to Agent → Use both RAG and API

---

**The key is understanding what data the user needs and routing to the appropriate source!** 🎯
