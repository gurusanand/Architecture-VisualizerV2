# Kafka Visibility Guide
## How to See Kafka Components in the Architecture Visualizer

---

## 🎯 Overview

Kafka and related messaging components are fully integrated into the architecture visualizer. This guide shows you how to see them in different views.

---

## 📨 Kafka Components in the System

The architecture includes **5 Kafka-related components**:

1. **📨 Kafka Broker** - Apache Kafka distributed event streaming platform
2. **🎯 Zookeeper** - Coordination service for Kafka cluster management
3. **🔄 Kafka Connect (Debezium)** - CDC connector for database change capture
4. **📊 Analytics Service** - Real-time analytics consuming agent execution events
5. **📝 Audit Service** - Comprehensive audit trail consuming all Kafka topics

---

## 🔍 How to View Kafka Components

### Method 1: Full Architecture Diagram

**Steps:**
1. Navigate to **"🏗️ Full Architecture"** in the sidebar
2. Look for the **"Layer Filters"** section
3. **Enable** the checkbox for **"Messaging & Streaming"**
4. Scroll down to see the architecture diagram
5. You'll see all 5 Kafka components with their connections

**What You'll See:**
- **Kafka Broker** (📨) in the center of the messaging layer
- **Zookeeper** (🎯) coordinating Kafka
- **Kafka Connect** (🔄) capturing database changes
- **Analytics Service** (📊) consuming agent events
- **Audit Service** (📝) consuming all events

**Connections:**
- Agents → Kafka (execution events)
- Governance → Kafka (compliance alerts)
- MCP Tools → Kafka (external events)
- Databases → Kafka Connect → Kafka (CDC events)
- Kafka → Analytics Service (agent events)
- Kafka → Audit Service (all events)
- Kafka → Observability (metrics)

---

### Method 2: Component Explorer

**Steps:**
1. Navigate to **"🔍 Component Explorer"** in the sidebar
2. In the **"Filter by Layer"** dropdown, select **"Messaging & Streaming"**
3. You'll see all 5 Kafka components listed

**For Each Component, You Can:**
- Click **"Show Details"** to expand
- See **Technical** explanation (for developers)
- See **Layman** explanation (for business users)
- View **Deployment Type** (⭐ Container or ☁️ Managed Service)
- See **Database Operations** (if applicable)
- See **Function Calls** (if applicable)
- See **API Integrations** (if applicable)

**Example - Kafka Broker Details:**
- **Technical**: "Apache Kafka distributed event streaming platform (Confluent 7.5.0) with 6 topics for async communication, CDC events, agent executions, compliance alerts, and external integrations. Supports 10K+ msgs/sec with <10ms latency"
- **Layman**: "Message delivery system that allows different parts of the system to communicate asynchronously, like an internal postal service"
- **Deployment**: ☁️ Container (Azure Kubernetes Service)
- **Protocols**: Kafka Protocol (port 9092 internal, 9093 external)

---

### Method 3: Request Flow Simulator

**Steps:**
1. Navigate to **"🚀 Request Flow Simulator"** in the sidebar
2. Select **"Card Application"** from the dropdown
3. Enable **"Animate Flow"** (optional)
4. Scroll down to see the flow diagram

**What You'll See:**
- The flow includes Kafka in the path
- **Step 22**: Card Agent → Kafka (publishes execution event)
- **Step 23**: Kafka → Audit Service (streams event for logging)
- **Step 27**: Governance → Kafka (publishes compliance alert)

**Flow with Kafka:**
```
... → Card Agent → Kafka → Audit Service → Card Agent 
→ Executor → Critic → Governance → Kafka → Planner → ...
```

---

### Method 4: Overview Page

**Steps:**
1. Navigate to **"🏠 Overview"** (default page)
2. Scroll down to **"Component Statistics"**
3. You'll see the count includes Kafka components

**Statistics:**
- **Total Components**: 35 (includes 5 Kafka components)
- **Microservices in AKS**: 13 (includes Analytics and Audit services)
- **Managed Services**: 9 (includes Kafka, Zookeeper, Kafka Connect)
- **External APIs**: 4

---

## 📊 Kafka Topics and Data Flows

### 6 Kafka Topics

1. **db.changes.users** - User database changes (CDC)
   - Source: MongoDB/PostgreSQL → Kafka Connect → Kafka
   - Consumers: Audit Service, Analytics Service

2. **db.changes.conversations** - Conversation history changes (CDC)
   - Source: MongoDB → Kafka Connect → Kafka
   - Consumers: Audit Service

3. **agent.executions** - Agent execution events
   - Source: Card Agent, Loan Agent, Wealth Agent → Kafka
   - Consumers: Analytics Service, Audit Service, Observability

4. **compliance.alerts** - Compliance alerts
   - Source: Governance → Kafka
   - Consumers: Audit Service, Observability

5. **external.crm.events** - CRM integration events
   - Source: MCP Tools → Kafka (when calling CRM)
   - Consumers: Audit Service, Analytics Service

6. **external.market.data** - Market data events
   - Source: MCP Tools → Kafka (when fetching market data)
   - Consumers: Analytics Service

---

## 🔄 Kafka Event Flows

### Flow 1: Agent Execution Event
```
Card Agent executes task
  ↓
Publishes to Kafka topic: "agent.executions"
  ↓
Kafka streams to:
  → Analytics Service (performance metrics)
  → Audit Service (compliance logging)
  → Observability (monitoring dashboards)
```

### Flow 2: Database Change Event (CDC)
```
User profile updated in MongoDB
  ↓
Kafka Connect (Debezium) captures change
  ↓
Publishes to Kafka topic: "db.changes.users"
  ↓
Kafka streams to:
  → Audit Service (immutable audit trail)
  → Analytics Service (user behavior analysis)
```

### Flow 3: Compliance Alert
```
Governance detects PII in response
  ↓
Publishes to Kafka topic: "compliance.alerts"
  ↓
Kafka streams to:
  → Audit Service (compliance logging)
  → Observability (alert dashboards)
```

---

## 🎨 Visual Indicators

### In Architecture Diagrams

**Kafka Components Have:**
- **Dark background** (messaging layer color: #FCE4EC)
- **Unique icons**: 📨 (Kafka), 🎯 (Zookeeper), 🔄 (Kafka Connect), 📊 (Analytics), 📝 (Audit)
- **Deployment badges**: ☁️ (Container/Managed Service)

**Kafka Connections Have:**
- **Dashed lines** (async/event-driven)
- **Labels** showing event types:
  - "Execution Events"
  - "Compliance Alerts"
  - "CDC Events"
  - "External Events"
  - "Agent Events"
  - "All Events"
  - "Metrics"

---

## 💡 Why Kafka Might Not Be Visible

### Common Reasons

1. **Layer Filter Disabled**
   - Solution: Enable "Messaging & Streaming" layer in Full Architecture

2. **Wrong Page**
   - Solution: Kafka is most visible in Full Architecture and Component Explorer

3. **Sample Query Doesn't Include Kafka**
   - Solution: Select "Card Application" or "Loan Inquiry" in Request Flow Simulator

4. **Diagram Too Large**
   - Solution: Use browser zoom (Ctrl + Mouse Wheel) to see all components

---

## 🔧 Technical Details

### Kafka Infrastructure

**Deployment:**
- **Kafka Broker**: Azure Kubernetes Service (AKS) - 3 replicas
- **Zookeeper**: Azure Kubernetes Service (AKS) - 3 replicas
- **Kafka Connect**: Azure Kubernetes Service (AKS) - 2 replicas
- **Analytics Service**: AKS microservice - 2 replicas
- **Audit Service**: AKS microservice - 3 replicas

**Configuration:**
- **Kafka Version**: Confluent Platform 7.5.0
- **Replication Factor**: 3
- **Partitions**: 6 per topic
- **Retention**: 7 days (agent.executions), 90 days (compliance.alerts), indefinite (audit logs)
- **Throughput**: 10K+ messages/sec
- **Latency**: <10ms (producer to broker), <100ms (end-to-end)

**Ports:**
- Kafka: 9092 (internal), 9093 (external)
- Zookeeper: 2181
- Kafka Connect: 8083

**Protocols:**
- Kafka Protocol (binary)
- Zookeeper Protocol
- HTTP/REST (Kafka Connect API)

---

## ✅ Verification Checklist

To verify Kafka is properly integrated:

- [ ] Can see Kafka Broker in Full Architecture (with Messaging layer enabled)
- [ ] Can see all 5 Kafka components in Component Explorer (filter by Messaging layer)
- [ ] Can see Kafka in Card Application flow path
- [ ] Can expand Kafka Broker details and see technical/layman explanations
- [ ] Can see Kafka connections with labels (Execution Events, Compliance Alerts, etc.)
- [ ] Can see deployment badge (☁️) on Kafka components
- [ ] Can see Kafka topics listed in component details
- [ ] Can see Kafka event flows in documentation

---

## 📚 Related Documentation

- **KAFKA_INTEGRATION_SUMMARY.md** - Complete Kafka integration details
- **ACTUAL_CODE_COMPONENTS.md** - Code-level Kafka implementation
- **AKS_DEPLOYMENT_SPEC.md** - Kafka deployment specifications
- **COMPLETE_FEATURE_SUMMARY.md** - All visualizer features

---

## 🎯 Quick Reference

**To see Kafka quickly:**

1. **Full Architecture** → Enable "Messaging & Streaming" layer → See diagram
2. **Component Explorer** → Filter by "Messaging & Streaming" → See 5 components
3. **Request Flow Simulator** → Select "Card Application" → See Kafka in path

**Kafka is there - just need to enable the right filters!** 📨
