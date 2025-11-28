# Enterprise Agent Platform - Architecture Visualizer v2.0

## 🚀 New Features in Version 2.0

### 1. **Authentication System** 🔐
- Secure login page with hardcoded credentials
- Session management with logout functionality
- Failed login attempt tracking
- Professional login interface

**Login Credentials:**
- **Username**: `CCArchitecture`
- **Password**: `DreamBig88$`

### 2. **OpenAPI Key Configuration** 🔑
- Secure API key input in sidebar
- Password-masked input field
- Session-based key storage
- Visual confirmation of configured keys

### 3. **High Level Architecture Slides** 📐
- Displays 4 high-level design slides
- Interactive navigation (slider, buttons, thumbnails)
- Full-screen view option
- Export to PDF/PPTX functionality

## 📋 Complete Feature List

### Core Features
- **32 Components** across 8 architectural layers
- **Interactive Diagrams** with Graphviz visualization
- **Bidirectional Flow Visualization** (request and response paths)
- **Deployment Architecture Markers**:
  - ⭐ Containerized microservices
  - ☁️ Managed services
  - 🌐 External APIs

### Pages & Views

1. **🏠 Overview**
   - Platform introduction
   - Key capabilities
   - Architecture statistics

2. **🔍 Component Explorer**
   - Browse all 32 components
   - Filter by layer
   - Technical and layman explanations
   - Deployment type indicators

3. **🧠 Planner Agent Details**
   - Deep dive into the Planner Agent
   - Decision-making process
   - Function calling capabilities

4. **🚀 Request Flow Simulator**
   - Simulate real queries
   - Step-by-step flow visualization
   - Sample queries included

5. **🎯 Numbered Flows**
   - Sequential flow diagrams
   - Request and response paths
   - Flow summaries

6. **📊 Full Architecture**
   - Complete system diagram
   - Layer filtering
   - Component relationships

7. **📝 Decision Flow Tables**
   - Detailed decision matrices
   - Agent interactions
   - Database operations

8. **🤖 OpenAPI Prompts**
   - LLM system prompts
   - User prompts for 6 stages
   - Prompt engineering examples

9. **📐 High Level Architecture** ⭐ NEW
   - 4 high-level design slides
   - Interactive navigation
   - Export capabilities

10. **✈️ Use Case: Airport Transfer**
    - 22-step journey visualization
    - Real-world scenario
    - Complete flow from request to completion

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.x
- **Visualization**: Graphviz
- **Authentication**: Custom session-based auth
- **Data Storage**: JSON files
- **Image Processing**: PIL, pdf2image
- **Python Version**: 3.11+

## 📦 Installation & Deployment

### Prerequisites
```bash
# Python 3.11 or higher
python3 --version

# Install dependencies
pip3 install streamlit graphviz pillow pdf2image
```

### Quick Start
```bash
# Extract the archive
tar -xzf architecture-visualizer-v2-final.tar.gz
cd architecture-visualizer

# Run the application
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Access the Application
1. Open browser to `http://localhost:8501`
2. Login with credentials:
   - Username: `CCArchitecture`
   - Password: `DreamBig88$`
3. Navigate through the sidebar menu

## 🔒 Security Features

- **Authentication Required**: All pages require login
- **Session Management**: Secure session state handling
- **Password Hashing**: SHA-256 hashing for credentials
- **API Key Protection**: Masked input for OpenAPI keys
- **Logout Functionality**: Clean session termination

## 📊 Architecture Overview

### Component Breakdown
- **11 Containerized Microservices** ⭐
- **5 Managed Services** ☁️
- **4 External APIs** 🌐
- **12 Supporting Components**

### Communication Protocols
- **HTTPS/REST**: API Gateway ↔ Services
- **gRPC**: Inter-service communication
- **Redis Pub/Sub**: Event streaming
- **Database Protocols**: PostgreSQL, Redis, Vector DB

### Layers
1. **Client Layer**: Web/Mobile interfaces
2. **API Gateway Layer**: Kong API Gateway
3. **Agent Orchestration Layer**: Coordinator, Planner, Executor
4. **Specialized Agents Layer**: Domain-specific agents
5. **Integration Layer**: MCP servers, RAG, Tools
6. **Data Layer**: Databases and caches
7. **External Services Layer**: LLMs, APIs
8. **Infrastructure Layer**: Monitoring, logging

## 🎨 Customization

### Modifying Components
Edit `architecture_data.py` to add/modify components:
```python
COMPONENTS = {
    "component_id": {
        "name": "Component Name",
        "layer": "layer_id",
        "type": "container",  # or "managed" or "external"
        "technical": "Technical description",
        "layman": "Simple explanation"
    }
}
```

### Adding Flows
Add new flows in `architecture_data.py`:
```python
FLOWS = [
    {
        "from": "source_component",
        "to": "target_component",
        "label": "Flow description",
        "protocol": "HTTPS/REST"
    }
]
```

### Updating Slides
Replace images in `hld_slides/` directory:
- `slide_1.png` through `slide_4.png`
- Recommended resolution: 1500x1125 (150 DPI)
- Format: PNG

## 📝 Configuration Files

### Key Files
- `app.py`: Main application entry point
- `auth.py`: Authentication module
- `architecture_data.py`: Component and flow definitions
- `hld_page.py`: High-level architecture slide viewer
- `prompt_display.py`: OpenAPI prompts page
- `airport_transfer_page.py`: Use case visualization
- `enhanced_component_details.json`: Extended component metadata

### Environment Variables
```bash
# Optional: Configure Streamlit
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 🐛 Troubleshooting

### Login Issues
- Ensure credentials are exactly: `CCArchitecture` / `DreamBig88$`
- Clear browser cache and cookies
- Check Streamlit logs for errors

### Missing Menu Items
- Clear Streamlit cache: `rm -rf ~/.streamlit/cache`
- Restart the application
- Verify all Python modules are imported correctly

### Slide Display Issues
- Verify `hld_slides/` directory contains PNG files
- Check file permissions: `chmod 644 hld_slides/*.png`
- Ensure PIL/Pillow is installed: `pip3 install pillow`

### Performance Issues
- Reduce diagram complexity by filtering layers
- Clear browser cache
- Restart Streamlit application

## 📈 Usage Statistics

### Current Scale
- **32 Components** documented
- **50+ Flows** mapped
- **8 Layers** defined
- **22 Steps** in Airport Transfer use case
- **6 Stages** of OpenAPI prompts
- **4 HLD Slides** included

## 🔄 Version History

### Version 2.0 (Current)
- ✅ Added authentication system
- ✅ Added OpenAPI key configuration
- ✅ Integrated high-level architecture slides
- ✅ Enhanced security features
- ✅ Improved UI/UX

### Version 1.0
- Initial release
- 32 components
- Basic flow visualization
- Component explorer
- Request simulator

## 📞 Support & Contact

For issues, questions, or feature requests:
- Check the troubleshooting section above
- Review the configuration files
- Examine Streamlit logs: `streamlit.log`

## 📄 License

Enterprise Internal Use Only - Confidential

---

**Version**: 2.0  
**Last Updated**: November 2024  
**Maintainer**: Enterprise Architecture Team
