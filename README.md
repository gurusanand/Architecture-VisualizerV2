# Enterprise Agent Platform - Architecture Visualizer

An interactive Streamlit application that visualizes the Enterprise Agent Platform architecture and demonstrates how requests flow through the system.

## Features

### 🏠 Overview
- High-level platform introduction
- Architecture layers explanation
- Platform statistics and capabilities

### 🔍 Component Explorer
- Detailed information for each component
- Filter by layer or search by name
- Technical and layman explanations
- Component connections and relationships

### 🚀 Request Flow Simulator
- Interactive request flow visualization
- Sample queries for different scenarios:
  - Card applications
  - Loan inquiries
  - Investment advice
  - General questions
  - Multi-intent queries
- Custom query input with automatic intent detection
- Animated step-by-step flow
- Flow diagrams showing the complete path

### 📊 Full Architecture Diagram
- Complete system architecture visualization
- Layer filtering
- Component highlighting
- Configurable diagram direction
- Interactive Graphviz diagrams

## Installation

### Prerequisites
- Python 3.11+
- Graphviz system library

### Install Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
Download and install from https://graphviz.org/download/

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

### Exploring Components

1. Navigate to **Component Explorer** from the sidebar
2. Filter by layer or search for specific components
3. Click on any component to see:
   - Technical explanation (for developers)
   - Layman explanation (for business users)
   - Incoming and outgoing connections

### Simulating Request Flows

1. Navigate to **Request Flow Simulator**
2. Choose a sample query or enter your own
3. Enable "Animate Flow" to see step-by-step processing
4. View the flow explanation and diagram

### Viewing Full Architecture

1. Navigate to **Full Architecture Diagram**
2. Select which layers to display
3. Highlight specific components
4. Choose diagram direction (Top-to-Bottom or Left-to-Right)

## Architecture Layers

The platform is organized into 8 layers:

1. **Entry Layer**: Customer interface and authentication
2. **Security Layer**: WAF, rate limiting, content filtering
3. **Orchestration Layer**: Request planning and execution
4. **Agent Layer**: Specialized domain agents
5. **Support Services**: Memory, RAG, tools, governance
6. **Data Layer**: Databases and caching
7. **External Services**: AI models and integrations
8. **Monitoring**: Observability and metrics

## Sample Queries

The visualizer includes pre-configured sample queries:

- **Card Application**: "I want to apply for a new credit card with travel rewards"
- **Loan Inquiry**: "What are my options for a home loan with $50,000 down payment?"
- **Investment Advice**: "Should I invest in stocks or bonds given my age and risk tolerance?"
- **General Question**: "What are your business hours?"
- **Multi-Intent Query**: "I want to check my credit card balance and also apply for a personal loan"

## Component Explanations

Each component includes:

- **Icon**: Visual identifier
- **Name**: Component name
- **Layer**: Architectural layer
- **Technical Explanation**: Detailed technical description for developers
- **Layman Explanation**: Simple explanation for non-technical users
- **Connections**: Incoming and outgoing data flows

## Customization

### Adding New Components

Edit `architecture_data.py` and add to the `COMPONENTS` dictionary:

```python
"new_component": {
    "name": "Component Name",
    "layer": "layer_id",
    "technical": "Technical explanation...",
    "layman": "Simple explanation...",
    "color": "#HEX_COLOR",
    "icon": "🎯"
}
```

### Adding New Flows

Add to the `FLOWS` list in `architecture_data.py`:

```python
{"from": "source_component", "to": "target_component", "label": "Flow Label"}
```

### Adding Sample Queries

Add to the `SAMPLE_QUERIES` dictionary in `architecture_data.py`:

```python
"Query Name": {
    "query": "The actual query text",
    "intent": "intent_type",
    "path": ["component1", "component2", ...],
    "explanation": "How this query is processed..."
}
```

## Technology Stack

- **Streamlit**: Web application framework
- **Graphviz**: Graph visualization library
- **Python 3.11+**: Programming language

## Architecture Reference

This visualizer is based on the Enterprise Agent Platform architecture which includes:

- Multi-agent orchestration using LangGraph
- Azure OpenAI integration
- Enterprise security (Azure AD, WAF, mTLS)
- Memory management (episodic and semantic)
- RAG (Retrieval-Augmented Generation)
- Governance and compliance
- Distributed tracing and observability

## License

This visualizer is part of the Enterprise Agent Platform project.

## Support

For questions or issues, please refer to the main Enterprise Agent Platform documentation.
