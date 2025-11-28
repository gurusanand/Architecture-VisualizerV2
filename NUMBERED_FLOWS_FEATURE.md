# Numbered Flows Feature
## Color-Coded Flow Visualization with Sequential Numbering

---

## 🎯 Overview

The Numbered Flows feature provides a crystal-clear visualization of two different data retrieval patterns in the Enterprise Agent Platform, using color-coded arrows with sequential numbering to show the complete request and response flow.

---

## 🎨 Color Coding

### 🟢 Dark Green Flow - RAG Knowledge Retrieval
- **Color**: #006400 (Dark Green)
- **Steps**: 11
- **Use Case**: "What are your business hours?"
- **Purpose**: Retrieve static knowledge from vector database
- **Latency**: ~200ms

### 🔵 Blue Flow - MCP Tool Call to Accounts API
- **Color**: #0066CC (Blue)
- **Steps**: 21
- **Use Case**: "Check my account balance"
- **Purpose**: Real-time API call to backend system
- **Latency**: ~512ms

---

## 📊 Flow Comparison

| Aspect | 🟢 RAG Flow | 🔵 MCP Flow |
|--------|-------------|-------------|
| **Total Steps** | 11 | 21 |
| **Latency** | ~200ms | ~512ms |
| **Data Source** | Vector DB (static) | Accounts API (real-time) |
| **Agent Involved** | No | Yes (Wealth Agent) |
| **LLM Call** | No | Yes (Azure OpenAI) |
| **External API** | No | Yes (Accounts API) |
| **Governance Check** | No | Yes |
| **Memory Context** | No | Yes |
| **Complexity** | Simple | Complex |

---

## 🟢 RAG Flow Detailed Steps (11 Total)

### Forward Path (Request)
1. **Customer → Authentication** (HTTPS/REST)
2. **Authentication → API Gateway** (JWT Token)
3. **API Gateway → Planner** (HTTP/REST)
4. **Planner → Tool Selector** (Intent classification)
5. **Tool Selector → RAG Engine** (Search request)
6. **RAG Engine → Vector DB** (Semantic query)
7. **Vector DB → RAG Engine** (Search results)

### Backward Path (Response)
8. **RAG Engine → Tool Selector** (Knowledge results)
9. **Tool Selector → Planner** (Formatted answer)
10. **Planner → API Gateway** (Final response)
11. **API Gateway → Customer** (Response delivery)

**Total Time**: ~200ms  
**Components Involved**: 6  
**External Calls**: 0

---

## 🔵 MCP Flow Detailed Steps (21 Total)

### Forward Path (Request)
1. **Customer → Authentication** (HTTPS/REST)
2. **Authentication → API Gateway** (JWT Token)
3. **API Gateway → Planner** (HTTP/REST)
4. **Planner → Memory Manager** (Retrieve context)
5. **Memory Manager → Planner** (User context data)
6. **Planner → Tool Selector** (Intent classification)
7. **Tool Selector → Executor** (Tool selection)
8. **Executor → Wealth Agent** (gRPC streaming)
9. **Wealth Agent → Azure OpenAI** (Parameter extraction)
10. **Azure OpenAI → Wealth Agent** (account_id extracted)
11. **Wealth Agent → MCP Tools** (get_account_balance request)
12. **MCP Tools → Accounts API** (GET /api/v1/accounts/{id}/balance + OAuth 2.0)
13. **Accounts API → MCP Tools** (Balance data)

### Backward Path (Response)
14. **MCP Tools → Wealth Agent** (Balance data)
15. **Wealth Agent → Executor** (Formatted response)
16. **Executor → Critic** (Validation request)
17. **Critic → Governance** (Compliance check)
18. **Governance → Critic** (Compliance OK)
19. **Critic → Planner** (Validated response)
20. **Planner → API Gateway** (Final response)
21. **API Gateway → Customer** (Response delivery)

**Total Time**: ~512ms  
**Components Involved**: 12  
**External Calls**: 2 (Azure OpenAI + Accounts API)

---

## 🎨 Visualization Features

### Numbered Arrows
- Each arrow is labeled with a number (1, 2, 3, ...)
- Numbers show the exact sequence of the flow
- Easy to follow the complete path from start to finish

### Color Coding
- **Dark Green (#006400)**: RAG flow arrows and labels
- **Blue (#0066CC)**: MCP flow arrows and labels
- **Bold lines**: 3.0 penwidth for visibility
- **Contrasting colors**: Easy to distinguish between flows

### Interactive Options

#### Flow Selection
- **Both Flows**: Show both RAG and MCP flows on same diagram
- **RAG Flow Only**: Show only the dark green RAG flow
- **MCP Flow Only**: Show only the blue MCP flow

#### Diagram Orientation
- **Horizontal (Left to Right)**: Better for wide screens
- **Vertical (Top to Bottom)**: Better for tall screens, easier to follow sequential steps

### Legend
Each diagram includes a legend explaining:
- 🟢 Dark Green: RAG Knowledge Retrieval with example query
- 🔵 Blue: MCP Tool Call to Accounts API with example query
- Numbers show the sequence of steps
- Colors distinguish different flow types

---

## 📋 Step-by-Step Breakdown

The page includes two tabs with detailed breakdowns:

### Tab 1: 🟢 RAG Flow Steps
- Lists all 11 steps with icons
- Shows component names
- Displays protocols used
- Explains actions taken

### Tab 2: 🔵 MCP Flow Steps
- Lists all 21 steps with icons
- Shows component names
- Displays protocols used
- Explains actions taken

---

## 💡 Use Cases

### When to Use RAG Flow (Green)
- **FAQs**: "What are your business hours?"
- **Policies**: "What is your refund policy?"
- **Product Info**: "What credit cards do you offer?"
- **General Knowledge**: "How do I reset my password?"

**Characteristics**:
- Static information
- No personalization needed
- Fast response (<200ms)
- No external API calls

### When to Use MCP Flow (Blue)
- **Account Data**: "Check my account balance"
- **Transactions**: "Show my recent transactions"
- **Personal Info**: "What's my credit limit?"
- **Real-time Data**: "What's my current loan balance?"

**Characteristics**:
- Real-time data
- Personalized to user
- Slower response (~512ms)
- External API calls required
- Governance and compliance checks

---

## 🔧 Technical Implementation

### Architecture Data (architecture_data.py)
```python
RAG_FLOW = [
    {"from": "customer", "to": "authentication", "step": 1, "label": "HTTPS/REST", "color": "#006400"},
    {"from": "authentication", "to": "api_gateway", "step": 2, "label": "JWT Token", "color": "#006400"},
    # ... 11 steps total
]

MCP_FLOW = [
    {"from": "customer", "to": "authentication", "step": 1, "label": "HTTPS/REST", "color": "#0066CC"},
    {"from": "authentication", "to": "api_gateway", "step": 2, "label": "JWT Token", "color": "#0066CC"},
    # ... 21 steps total
]
```

### Diagram Generation (numbered_flow_diagram.py)
```python
def create_numbered_flow_diagram(flow_type: str = "both") -> graphviz.Digraph:
    """Create architecture diagram with numbered, color-coded flows"""
    # Creates nodes for all components
    # Adds colored edges with numbers
    # Includes legend
    # Returns Graphviz diagram
```

### Streamlit Page (app.py)
```python
def show_numbered_flows():
    """Display numbered flow diagrams with color coding"""
    # Flow selection dropdown
    # Orientation selection
    # Flow comparison tables
    # Diagram display
    # Step-by-step breakdown tabs
```

---

## 📊 Diagram Examples

### Both Flows (Default View)
Shows both RAG (green) and MCP (blue) flows on the same diagram, allowing direct visual comparison of the two patterns.

**Benefits**:
- Compare complexity visually
- See shared components
- Understand decision points
- Identify optimization opportunities

### RAG Flow Only
Shows only the dark green RAG flow for clarity when explaining knowledge retrieval.

**Benefits**:
- Cleaner diagram
- Focus on knowledge retrieval
- Easier to explain to non-technical users
- Better for presentations

### MCP Flow Only
Shows only the blue MCP flow for clarity when explaining API integration.

**Benefits**:
- Cleaner diagram
- Focus on API integration
- Shows governance and compliance
- Better for technical deep-dives

---

## 🎯 Key Insights from Visualization

### 1. Complexity Difference
- RAG flow: 11 steps, simple path
- MCP flow: 21 steps, complex orchestration
- **Insight**: Real-time data requires more infrastructure

### 2. Latency Factors
- RAG: No external calls = faster
- MCP: Multiple external calls = slower
- **Insight**: Static knowledge is faster to retrieve

### 3. Security & Governance
- RAG: No governance checks
- MCP: Full governance pipeline
- **Insight**: Real-time data requires more controls

### 4. Agent Involvement
- RAG: Direct path, no agents
- MCP: Wealth Agent orchestrates
- **Insight**: Complex queries need intelligent routing

### 5. LLM Usage
- RAG: No LLM needed
- MCP: Azure OpenAI for parameter extraction
- **Insight**: LLM adds intelligence but also latency

---

## ✅ Benefits of Numbered Flows

### For Developers
- Understand exact execution sequence
- Debug issues by step number
- Optimize specific steps
- Identify bottlenecks

### For Architects
- Compare architectural patterns
- Make design decisions
- Explain trade-offs
- Document flows

### For Business Users
- Understand why some queries are slower
- See the value of different approaches
- Make informed feature requests
- Appreciate system complexity

### For Executives
- Visual proof of architecture rigor
- Clear explanation of latency differences
- Justification for infrastructure costs
- Confidence in system design

---

## 🚀 Future Enhancements

### Potential Additions
1. **Animation**: Highlight steps sequentially with timing
2. **More Flows**: Add Card Application flow, Loan Inquiry flow
3. **Timing Overlay**: Show actual timing for each step
4. **Error Paths**: Show what happens when steps fail
5. **Parallel Paths**: Show concurrent operations
6. **Database Queries**: Overlay actual queries on each step
7. **Cost Analysis**: Show cost per step (API calls, compute)
8. **Comparison Mode**: Side-by-side comparison of multiple flows

---

## 📚 Files Added/Modified

### New Files
1. **numbered_flow_diagram.py** (6KB)
   - create_numbered_flow_diagram()
   - create_numbered_flow_diagram_vertical()
   - get_flow_summary()

2. **NUMBERED_FLOWS_DESIGN.md** (8KB)
   - Design documentation
   - Flow definitions
   - Implementation strategy

3. **NUMBERED_FLOWS_FEATURE.md** (this file, 12KB)
   - Feature documentation
   - User guide
   - Technical details

### Modified Files
1. **architecture_data.py**
   - Added RAG_FLOW (11 steps)
   - Added MCP_FLOW (21 steps)

2. **app.py**
   - Added show_numbered_flows() function
   - Added "🎯 Numbered Flows" to navigation
   - Imported numbered flow functions

---

## 🎓 How to Use

### Step 1: Navigate to Numbered Flows
- Open the visualizer
- Click "🎯 Numbered Flows" in the sidebar

### Step 2: Select Flow Type
- Choose "Both Flows" to compare
- Choose "RAG Flow Only" for knowledge retrieval
- Choose "MCP Flow Only" for API integration

### Step 3: Choose Orientation
- Select "Horizontal" for wide screens
- Select "Vertical" for better sequential view

### Step 4: Review Comparison
- Check the flow comparison table
- Compare steps, latency, components

### Step 5: Study Diagram
- Follow the numbered arrows
- Note the color coding
- Read the legend

### Step 6: Explore Details
- Click "🟢 RAG Flow Steps" tab for details
- Click "🔵 MCP Flow Steps" tab for details
- Read step-by-step breakdown

---

## ✅ Summary

**The Numbered Flows feature provides:**

✅ **Visual Clarity**: Color-coded flows with sequential numbers  
✅ **Complete Paths**: Full request and response sequences  
✅ **Easy Comparison**: Side-by-side flow analysis  
✅ **Detailed Breakdown**: Step-by-step explanations  
✅ **Interactive Options**: Multiple view modes  
✅ **Professional Design**: Production-ready visualizations  

**Perfect for:**
- Architecture reviews
- Technical presentations
- Developer onboarding
- Executive briefings
- Documentation
- Debugging sessions

**The numbered flows make complex architecture easy to understand at a glance!** 🎯
