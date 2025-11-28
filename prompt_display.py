"""
Prompt Display Module
Shows system and user prompts for OpenAPI-based architecture
"""

import streamlit as st
import json

def show_openapi_prompts():
    """Display OpenAPI prompts for all components"""
    
    st.title("🤖 OpenAPI Architecture: LLM Prompts")
    
    st.markdown("""
    When using **OpenAPI-based architecture**, the system uses LLM prompts at multiple stages 
    for dynamic API discovery, tool selection, and parameter extraction. This page shows the 
    exact prompts sent to the LLM.
    """)
    
    # OpenAPI Key Configuration Section
    st.markdown("---")
    with st.expander("🔑 OpenAPI Key Configuration & Testing", expanded=True):
        st.markdown("""
        Enter your OpenAPI key below to test the prompts with a live LLM. This allows you to:
        - Test prompt effectiveness
        - Validate response formats
        - Experiment with different queries
        - Measure token usage and latency
        """)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Initialize session state for API key if not exists
            if 'openapi_key_prompts_page' not in st.session_state:
                st.session_state.openapi_key_prompts_page = ""
            
            api_key_input = st.text_input(
                "OpenAPI Key",
                value=st.session_state.openapi_key_prompts_page,
                type="password",
                placeholder="sk-...",
                help="Enter your OpenAPI key to enable live testing of prompts",
                key="api_key_input_field"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save Key"):
                st.session_state.openapi_key_prompts_page = api_key_input
                st.success("✅ API Key saved!")
                st.rerun()
        
        # Display key status
        if st.session_state.openapi_key_prompts_page:
            key_length = len(st.session_state.openapi_key_prompts_page)
            masked_key = st.session_state.openapi_key_prompts_page[:7] + "..." + st.session_state.openapi_key_prompts_page[-4:] if key_length > 11 else "***"
            st.success(f"🔐 API Key configured: {masked_key} ({key_length} characters)")
            
            # Test prompt section
            st.markdown("### 🧪 Test a Prompt")
            
            test_stage = st.selectbox(
                "Select a stage to test:",
                ["Tool Selector", "Executor", "Agent Response Formatting"],
                help="Choose which LLM stage you want to test"
            )
            
            test_query = st.text_area(
                "Enter a test query:",
                value="What's my account balance?",
                help="Enter a sample user query to test the selected prompt"
            )
            
            if st.button("🚀 Test Prompt", type="primary"):
                with st.spinner(f"Testing {test_stage} prompt..."):
                    try:
                        # Import OpenAI library
                        from openai import OpenAI
                        
                        # Initialize client
                        client = OpenAI(api_key=st.session_state.openapi_key_prompts_page)
                        
                        # Prepare prompts based on stage
                        if test_stage == "Tool Selector":
                            system_prompt = """You are an API discovery assistant. Given a user query, identify which APIs should be called.

Available APIs:
- accounts_api_get_balance: Get account balance
- accounts_api_get_transactions: Get transaction history
- cards_api_list: List credit/debit cards
- loans_api_get_offers: Get loan offers

Respond with a JSON array of operation IDs."""
                            user_prompt = f"User query: {test_query}\n\nWhich APIs should be called?"
                        
                        elif test_stage == "Executor":
                            system_prompt = """You are a parameter extraction assistant. Extract required parameters from the user query and context.

API: accounts_api_get_balance
Parameters:
- account_id (required): string
- include_pending (optional): boolean

Respond with JSON containing the extracted parameters."""
                            user_prompt = f"User query: {test_query}\nUser context: {{\"user_id\": \"USER123\", \"primary_account\": \"ACC0000123456\"}}\n\nExtract parameters:"
                        
                        else:  # Agent Response Formatting
                            system_prompt = """You are a customer service assistant. Format API responses into natural, conversational messages.

Guidelines:
- Be conversational and friendly
- Use proper currency formatting
- Highlight important information
- Suggest relevant next actions"""
                            user_prompt = f"""User Query: {test_query}

API Response:
{{
  "account_id": "ACC0000123456",
  "balance": 15234.50,
  "currency": "AED",
  "as_of_date": "2024-01-15T10:30:00Z"
}}

Format this into a conversational response:"""
                        
                        # Make API call
                        import time
                        start_time = time.time()
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            temperature=0.7,
                            max_tokens=500
                        )
                        
                        end_time = time.time()
                        latency = (end_time - start_time) * 1000  # Convert to ms
                        
                        # Display results
                        st.success("✅ Test completed successfully!")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Latency", f"{latency:.0f}ms")
                        with col2:
                            st.metric("Tokens Used", response.usage.total_tokens)
                        with col3:
                            cost = (response.usage.prompt_tokens * 0.00015 + response.usage.completion_tokens * 0.0006) / 1000
                            st.metric("Cost (GPT-4o-mini)", f"${cost:.4f}")
                        
                        st.markdown("### 📤 LLM Response")
                        st.code(response.choices[0].message.content, language="text")
                        
                        st.markdown("#### 📊 Detailed Metrics")
                        st.json({
                            "model": response.model,
                            "prompt_tokens": response.usage.prompt_tokens,
                            "completion_tokens": response.usage.completion_tokens,
                            "total_tokens": response.usage.total_tokens,
                            "latency_ms": round(latency, 2),
                            "finish_reason": response.choices[0].finish_reason
                        })
                    
                    except ImportError:
                        st.error("❌ OpenAI library not installed. Run: `pip install openai`")
                    except Exception as e:
                        st.error(f"❌ Error testing prompt: {str(e)}")
                        st.info("Please check your API key and try again.")
        else:
            st.warning("⚠️ No API Key configured. Enter your key above to enable live testing.")
    
    st.markdown("---")
    
    # Load component details
    try:
        import os
        json_path = os.path.join(os.path.dirname(__file__), 'enhanced_component_details.json')
        with open(json_path, 'r') as f:
            details = json.load(f)
    except Exception as e:
        st.error(f"Could not load component details: {e}")
        return
    
    # Overview
    with st.expander("📊 Overview: 6 LLM Stages", expanded=True):
        st.markdown("""
        ### LLM Usage in OpenAPI Architecture
        
        The OpenAPI-based architecture uses LLMs at **6 distinct stages**:
        
        1. **Tool Selector** - API Discovery (Which APIs to call?)
        2. **OpenAPI Registry** - Schema Retrieval (What's the API spec?)
        3. **Executor** - Parameter Extraction (What parameters to send?)
        4. **OpenAPI Client** - Dynamic Code Generation (How to call the API?)
        5. **Schema Validator** - Response Validation (Is the response valid?)
        6. **Agent** - Response Formatting (How to present to user?)
        
        **Total Token Usage per Query**: ~3,650 tokens  
        **Cost (GPT-4)**: ~$0.11 per query  
        **Latency Overhead**: +100ms compared to code-based approach
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("LLM Calls", "6", "per query")
        with col2:
            st.metric("Tokens", "3,650", "per query")
        with col3:
            st.metric("Cost", "$0.11", "GPT-4")
    
    # Stage 1: Tool Selector
    st.markdown("---")
    st.header("1️⃣ Tool Selector: API Discovery")
    
    if 'tool_selector' in details and 'openapi_system_prompt' in details['tool_selector']:
        prompts = details['tool_selector']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔵 System Prompt")
            st.code(prompts['openapi_system_prompt'], language='text')
            
        with col2:
            st.subheader("🟢 User Prompt Template")
            st.code(prompts['openapi_user_prompt_template'], language='text')
        
        st.subheader("📤 Example Response")
        st.code(prompts['openapi_example_response'], language='json')
        
        with st.expander("💡 Explanation"):
            st.markdown("""
            **Purpose**: Analyze user query and identify which APIs are needed from the OpenAPI registry.
            
            **Input**:
            - User query: "What's my account balance?"
            - Context: User ID, session info
            - Available OpenAPI specs: List of all APIs
            
            **Output**: JSON array of operation IDs
            
            **Token Usage**: ~550 tokens (300 system + 200 user + 50 response)
            """)
    
    # Stage 2: OpenAPI Registry
    st.markdown("---")
    st.header("2️⃣ OpenAPI Registry: Schema Retrieval")
    
    if 'openapi_registry' in details and 'system_prompt' in details['openapi_registry']:
        prompts = details['openapi_registry']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔵 System Prompt")
            st.code(prompts['system_prompt'], language='text')
            
        with col2:
            st.subheader("🟢 User Prompt Template")
            st.code(prompts['user_prompt_template'], language='text')
        
        st.subheader("📤 Example Response")
        st.code("""openapi: 3.0.0
paths:
  /api/v1/accounts/{account_id}/balance:
    get:
      operationId: accounts_api_get_balance
      parameters:
        - name: account_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  balance: {type: number}
                  currency: {type: string}
      security:
        - OAuth2: [read:accounts]""", language='yaml')
        
        with st.expander("💡 Explanation"):
            st.markdown("""
            **Purpose**: Retrieve the complete OpenAPI specification for a given operation ID.
            
            **Input**: Operation ID (e.g., "accounts_api_get_balance")
            
            **Output**: Complete OpenAPI spec with endpoints, parameters, schemas, security
            
            **Token Usage**: ~550 tokens (100 system + 50 user + 400 response)
            """)
    
    # Stage 3: Executor
    st.markdown("---")
    st.header("3️⃣ Executor: Parameter Extraction")
    
    if 'executor' in details and 'openapi_system_prompt' in details['executor']:
        prompts = details['executor']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔵 System Prompt")
            st.code(prompts['openapi_system_prompt'], language='text')
            
        with col2:
            st.subheader("🟢 User Prompt Template")
            st.code(prompts['openapi_user_prompt_template'], language='text')
        
        st.subheader("📤 Example Response")
        st.code(prompts['openapi_example_response'], language='json')
        
        with st.expander("💡 Explanation"):
            st.markdown("""
            **Purpose**: Extract required parameters from user query and context to populate API request.
            
            **Input**:
            - API operation: accounts_api_get_balance
            - OpenAPI spec: Parameter definitions
            - User query: "What's my account balance?"
            - Context: User ID, account ID
            
            **Output**: JSON with extracted parameters
            
            **Token Usage**: ~650 tokens (250 system + 300 user + 100 response)
            """)
    
    # Stage 4: OpenAPI Client
    st.markdown("---")
    st.header("4️⃣ OpenAPI Client: Dynamic Code Generation")
    
    if 'openapi_client' in details and 'system_prompt' in details['openapi_client']:
        prompts = details['openapi_client']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔵 System Prompt")
            st.code(prompts['system_prompt'], language='text')
            
        with col2:
            st.subheader("🟢 User Prompt Template")
            st.code(prompts['user_prompt_template'], language='text')
        
        st.subheader("📤 Example Response")
        st.code("""import requests

def call_api(account_id, token):
    url = f"https://api.bank.com/api/v1/accounts/{account_id}/balance"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

result = call_api("ACC0000123456", "eyJhbGc...")""", language='python')
        
        with st.expander("💡 Explanation"):
            st.markdown("""
            **Purpose**: Generate Python code to make the API call based on OpenAPI spec.
            
            **Input**:
            - OpenAPI spec: Endpoint, method, parameters
            - Parameters: Extracted values
            - OAuth token: Authentication
            
            **Output**: Executable Python code using requests library
            
            **Token Usage**: ~700 tokens (200 system + 200 user + 300 response)
            """)
    
    # Stage 5: Schema Validator
    st.markdown("---")
    st.header("5️⃣ Schema Validator: Response Validation")
    
    if 'schema_validator' in details and 'system_prompt' in details['schema_validator']:
        prompts = details['schema_validator']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔵 System Prompt")
            st.code(prompts['system_prompt'], language='text')
            
        with col2:
            st.subheader("🟢 User Prompt Template")
            st.code(prompts['user_prompt_template'], language='text')
        
        st.subheader("📤 Example Response")
        st.code(prompts['example_response'], language='json')
        
        with st.expander("💡 Explanation"):
            st.markdown("""
            **Purpose**: Validate API response against OpenAPI schema.
            
            **Input**:
            - OpenAPI response schema: Expected structure
            - Actual API response: Data received
            
            **Output**: Validation report with errors and warnings
            
            **Token Usage**: ~650 tokens (200 system + 300 user + 150 response)
            """)
    
    # Stage 6: Agent
    st.markdown("---")
    st.header("6️⃣ Agent: Response Formatting")
    
    with st.expander("🔵 System Prompt", expanded=True):
        st.code("""You are a customer service assistant for a banking platform. Format API responses into natural, conversational messages for customers.

**Your Task:**
1. Review the API response data
2. Format it into a friendly, clear message
3. Include relevant details without overwhelming
4. Use appropriate formatting (currency, dates)
5. Add helpful context or next steps

**Guidelines:**
- Be conversational and friendly
- Use proper currency formatting
- Format dates in a readable way
- Highlight important information
- Suggest relevant next actions
- Keep messages concise but complete""", language='text')
    
    with st.expander("🟢 User Prompt Example"):
        st.code("""User Query: "What's my account balance?"

API Response:
{
  "account_id": "ACC0000123456",
  "balance": 15234.50,
  "currency": "AED",
  "as_of_date": "2024-01-15T10:30:00Z"
}

Format this into a conversational response for the customer.""", language='text')
    
    with st.expander("📤 Example Response"):
        st.markdown("""
Your savings account balance is **AED 15,234.50** as of today at 10:30 AM.

Would you like to:
- View recent transactions
- Transfer funds
- Set up a savings goal
        """)
    
    with st.expander("💡 Explanation"):
        st.markdown("""
        **Purpose**: Convert API response into user-friendly message.
        
        **Input**: Raw API response data
        
        **Output**: Formatted conversational response
        
        **Token Usage**: ~550 tokens (250 system + 200 user + 100 response)
        """)
    
    # Comparison
    st.markdown("---")
    st.header("📊 Comparison: Code-Based vs OpenAPI-Based")
    
    comparison_data = {
        "Aspect": ["LLM Calls", "Token Usage", "Cost (GPT-4)", "Latency", "Flexibility", "Type Safety"],
        "Code-Based": ["1-2", "~500", "$0.015", "412ms", "Low", "High"],
        "OpenAPI-Based": ["6", "~3,650", "$0.11", "512ms", "High", "Medium"]
    }
    
    import pandas as pd
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Token breakdown
    st.subheader("🔢 Token Usage Breakdown (OpenAPI-Based)")
    
    token_data = {
        "Stage": ["Tool Selector", "OpenAPI Registry", "Executor", "OpenAPI Client", "Schema Validator", "Agent", "Total"],
        "System": [300, 100, 250, 200, 200, 250, 1300],
        "User": [200, 50, 300, 200, 300, 200, 1250],
        "Response": [50, 400, 100, 300, 150, 100, 1100],
        "Total": [550, 550, 650, 700, 650, 550, 3650]
    }
    
    df_tokens = pd.DataFrame(token_data)
    st.dataframe(df_tokens, use_container_width=True, hide_index=True)
    
    # Documentation link
    st.markdown("---")
    st.info("📚 **Complete Documentation**: See `OPENAPI_PROMPTS.md` for detailed prompt engineering strategies, examples, and best practices.")
    
    # Additional testing tips
    with st.expander("💡 Testing Tips"):
        st.markdown("""
        ### Best Practices for Testing Prompts
        
        1. **Start Simple**: Test with basic queries before complex ones
        2. **Measure Tokens**: Monitor token usage to optimize costs
        3. **Compare Models**: Try different models (gpt-4o-mini, gpt-4o) to balance cost and quality
        4. **Iterate Prompts**: Refine system prompts based on test results
        5. **Test Edge Cases**: Try ambiguous queries, multi-intent queries, and error scenarios
        
        ### Sample Test Queries
        
        **Simple Queries:**
        - "What's my balance?"
        - "Show my recent transactions"
        - "List my credit cards"
        
        **Complex Queries:**
        - "I want to check my balance and apply for a loan"
        - "What are my investment options for retirement?"
        - "Transfer $500 from savings to checking and pay my credit card bill"
        
        **Edge Cases:**
        - "Hello" (no clear intent)
        - "asdfghjkl" (gibberish)
        - "What's the weather?" (out of scope)
        """)


if __name__ == "__main__":
    show_openapi_prompts()
