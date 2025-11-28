# Quick Start Guide - Architecture Visualizer

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

#### Install Graphviz (System Library)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
Download from https://graphviz.org/download/ and add to PATH

#### Install Python Packages

```bash
pip install streamlit graphviz
```

### Step 2: Run the Application

```bash
cd architecture-visualizer
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

### Step 3: Explore

1. **Start with Overview** - Get familiar with the platform
2. **Try Request Flow Simulator** - Select "Card Application" sample
3. **Explore Components** - Filter by "Security Layer"
4. **View Full Architecture** - See the complete system

---

## 🎯 What Can You Do?

### 1. Understand Components
- Search for any component (e.g., "API Gateway")
- Read technical and layman explanations
- See how components connect

### 2. Visualize Request Flows
- Try sample queries:
  - "I want to apply for a credit card"
  - "What loan options do I have?"
  - "Should I invest in stocks or bonds?"
- Enter your own custom queries
- Watch animated step-by-step processing

### 3. View Architecture
- See the complete system diagram
- Filter by layers
- Highlight specific components
- Export diagrams for presentations

---

## 📚 Sample Queries to Try

### Credit Card Query
```
I want to apply for a new credit card with travel rewards
```
**What you'll see**: Authentication → Security checks → Planner → Card Agent → AI processing → CRM integration → Response

### Loan Query
```
What are my options for a home loan with $50,000 down payment?
```
**What you'll see**: Security → Planning → Loan Agent → Knowledge base search → Calculation → Validation → Response

### Investment Query
```
Should I invest in stocks or bonds given my age and risk tolerance?
```
**What you'll see**: Authentication → Planning → Wealth Agent → Risk profiling → AI advice → Compliance check → Response

### Multi-Intent Query
```
I want to check my credit card balance and also apply for a personal loan
```
**What you'll see**: Intent decomposition → Parallel execution → Card Agent + Loan Agent → Result synthesis → Response

---

## 🎨 Navigation Tips

### Sidebar Menu
- **🏠 Overview**: Platform introduction
- **🔍 Component Explorer**: Detailed component info
- **🚀 Request Flow Simulator**: Interactive flow visualization
- **📊 Full Architecture**: Complete system diagram

### Color Coding
- **Blue boxes**: Entry and external components
- **Orange boxes**: Security components
- **Green boxes**: Orchestration components
- **Purple boxes**: Agent components
- **Teal boxes**: Support services
- **Red boxes**: Data layer
- **Yellow boxes**: Monitoring

### Icons
Each component has an emoji icon for quick recognition:
- 👤 Customer
- 🔐 Authentication
- 🚪 API Gateway
- 🛡️ Security
- 📋 Planner
- 💳 Card Agent
- 🏦 Loan Agent
- 💰 Wealth Agent
- 🧠 Memory
- 📚 Knowledge Base
- 🤖 AI/LLM

---

## 💡 Pro Tips

1. **Enable Animation**: Check "Animate Flow" in Request Flow Simulator for better presentations
2. **Use Search**: Quickly find components in Component Explorer
3. **Filter Layers**: Focus on specific aspects in Full Architecture
4. **Try Custom Queries**: Don't just use samples - try your own questions
5. **Read Both Explanations**: Technical for depth, Layman for clarity

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use a different port
streamlit run app.py --server.port 8502
```

### Graphviz Not Found
```bash
# Verify installation
dot -V

# If not found, reinstall
sudo apt-get install graphviz  # Linux
brew install graphviz          # macOS
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📖 Next Steps

### For Learning
1. Read the **USER_GUIDE.md** for detailed feature explanations
2. Review **TECHNICAL_DOCUMENTATION.md** for architecture deep dive
3. Explore the **architecture_data.py** to understand component definitions

### For Customization
1. Edit **architecture_data.py** to add/modify components
2. Modify **app.py** to add new features
3. Update **COMPONENTS** dictionary to change explanations

### For Presentations
1. Use Full Architecture diagram with highlighting
2. Use Request Flow Simulator with animation
3. Export diagrams (screenshot or print)
4. Prepare custom queries relevant to your audience

---

## 🌟 Key Features

✅ **Interactive Visualization** - Click, filter, and explore  
✅ **Dual Explanations** - Technical and layman terms  
✅ **Request Simulation** - See how queries are processed  
✅ **Complete Architecture** - Full system diagram  
✅ **Search & Filter** - Find what you need quickly  
✅ **Animation** - Step-by-step flow visualization  
✅ **Customizable** - Easy to extend and modify  

---

## 📞 Need Help?

- **User Guide**: See USER_GUIDE.md for detailed instructions
- **Technical Docs**: See TECHNICAL_DOCUMENTATION.md for architecture details
- **README**: See README.md for installation and customization

---

**Ready to explore? Launch the app and start with the Overview page! 🚀**
