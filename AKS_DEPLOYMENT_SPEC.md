# AKS Deployment Specification
## Enterprise Agent Platform - Kubernetes Architecture

---

## 🎯 Overview

The Enterprise Agent Platform runs on **Azure Kubernetes Service (AKS)** with 11 microservices deployed as containerized workloads. This document specifies which components run in AKS, their deployment configurations, and infrastructure dependencies.

---

## 📦 Components in AKS (Microservices)

### 1. API Gateway ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/api-gateway:v1.2.3`  
**Replicas**: 5  
**Resources**:
- CPU: 500m (request), 1000m (limit)
- Memory: 512Mi (request), 1Gi (limit)

**Protocols**:
- Inbound: HTTPS/REST (port 443)
- Outbound: HTTP/REST to internal services

**Service Type**: LoadBalancer (Azure Load Balancer)

---

### 2. Planner Agent ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/planner:v2.1.0`  
**Replicas**: 3  
**Resources**:
- CPU: 1000m (request), 2000m (limit)
- Memory: 1Gi (request), 2Gi (limit)

**Protocols**:
- Inbound: HTTP/REST (port 8080)
- Outbound: 
  - HTTP/REST to Memory Manager, Tool Selector
  - HTTPS to Azure OpenAI

**Environment Variables**:
- `AZURE_OPENAI_ENDPOINT`
- `MEMORY_MANAGER_URL`
- `TOOL_SELECTOR_URL`

---

### 3. Tool Selector ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/tool-selector:v1.5.2`  
**Replicas**: 3  
**Resources**:
- CPU: 300m (request), 500m (limit)
- Memory: 256Mi (request), 512Mi (limit)

**Protocols**:
- Inbound: HTTP/REST (port 8080)
- Outbound: HTTP/REST to Executor

**ConfigMap**: `mcp-tool-registry` (24 tool definitions)

---

### 4. Executor ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/executor:v1.8.1`  
**Replicas**: 5  
**Resources**:
- CPU: 500m (request), 1000m (limit)
- Memory: 512Mi (request), 1Gi (limit)

**Protocols**:
- Inbound: HTTP/REST (port 8080)
- Outbound: gRPC to Domain Agents (port 9090)

**Service Mesh**: Istio enabled for traffic management

---

### 5. Card Agent ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/card-agent:v2.0.5`  
**Replicas**: 3  
**Resources**:
- CPU: 800m (request), 1500m (limit)
- Memory: 768Mi (request), 1.5Gi (limit)

**Protocols**:
- Inbound: gRPC (port 9090)
- Outbound:
  - HTTPS to Azure OpenAI
  - HTTP/REST to MCP Tools
  - Redis Pub/Sub for agent coordination

**Environment Variables**:
- `AZURE_OPENAI_ENDPOINT`
- `MCP_TOOLS_URL`
- `REDIS_HOST`

---

### 6. Loan Agent ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/loan-agent:v2.0.5`  
**Replicas**: 3  
**Resources**:
- CPU: 800m (request), 1500m (limit)
- Memory: 768Mi (request), 1.5Gi (limit)

**Protocols**:
- Inbound: gRPC (port 9090)
- Outbound:
  - HTTPS to Azure OpenAI
  - HTTP/REST to MCP Tools, RAG Engine
  - Redis Pub/Sub for agent coordination

---

### 7. Wealth Agent ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/wealth-agent:v2.0.5`  
**Replicas**: 3  
**Resources**:
- CPU: 800m (request), 1500m (limit)
- Memory: 768Mi (request), 1.5Gi (limit)

**Protocols**:
- Inbound: gRPC (port 9090)
- Outbound:
  - HTTPS to Azure OpenAI
  - HTTP/REST to MCP Tools, RAG Engine
  - Redis Pub/Sub for agent coordination

---

### 8. Critic Agent ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/critic:v1.3.0`  
**Replicas**: 2  
**Resources**:
- CPU: 400m (request), 800m (limit)
- Memory: 512Mi (request), 1Gi (limit)

**Protocols**:
- Inbound: HTTP/REST (port 8080)
- Outbound: HTTPS to Azure OpenAI

---

### 9. Memory Manager ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/memory-manager:v1.6.0`  
**Replicas**: 3  
**Resources**:
- CPU: 600m (request), 1200m (limit)
- Memory: 1Gi (request), 2Gi (limit)

**Protocols**:
- Inbound: HTTP/REST (port 8080)
- Outbound:
  - MongoDB Wire Protocol (port 27017)
  - Redis RESP3 (port 6379)

**Persistent Storage**: Azure Disk for episodic memory cache

---

### 10. RAG Engine ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/rag-engine:v1.4.2`  
**Replicas**: 3  
**Resources**:
- CPU: 1000m (request), 2000m (limit)
- Memory: 2Gi (request), 4Gi (limit)

**Protocols**:
- Inbound: HTTP/REST (port 8080)
- Outbound:
  - PostgreSQL protocol to Vector DB (port 5432)
  - HTTPS to Azure OpenAI

**Persistent Storage**: Azure Disk for index cache

---

### 11. MCP Tools ⭐
**Deployment Type**: Container in AKS  
**Image**: `acr.azurecr.io/agent-platform/mcp-tools:v1.7.3`  
**Replicas**: 5  
**Resources**:
- CPU: 400m (request), 800m (limit)
- Memory: 512Mi (request), 1Gi (limit)

**Protocols**:
- Inbound: HTTP/REST (port 8080)
- Outbound:
  - HTTPS + OAuth 2.0 to Accounts API
  - HTTPS + OAuth 2.0 to Cards API
  - HTTPS + OAuth 2.0 to Loans API
  - HTTPS + OAuth 2.0 to CRM/ServiceNow

**Secrets**: `oauth-credentials` (OAuth 2.0 client ID/secret)

---

## ☁️ Managed Services (Azure PaaS)

### 1. Authentication (Azure AD) ☁️
**Service**: Azure Active Directory B2C  
**Purpose**: User authentication and JWT token issuance  
**Protocol**: OAuth 2.0 / OpenID Connect  
**Integration**: API Gateway validates JWT tokens

---

### 2. Redis Cache ☁️
**Service**: Azure Cache for Redis (Premium tier)  
**Purpose**: 
- Rate limiting counters
- Memory cache
- Agent coordination (Pub/Sub)

**Protocol**: Redis RESP3  
**Configuration**:
- Size: 6GB
- Clustering: Enabled (3 shards)
- Persistence: RDB snapshots every 15 minutes

---

### 3. Cosmos DB ☁️
**Service**: Azure Cosmos DB (MongoDB API)  
**Purpose**:
- Memory episodes
- Tool execution logs
- Audit trails

**Protocol**: MongoDB Wire Protocol  
**Configuration**:
- Consistency: Session
- Geo-replication: 2 regions (active-active)
- Throughput: 10,000 RU/s (autoscale)

---

### 4. Vector DB (PostgreSQL) ☁️
**Service**: Azure Database for PostgreSQL with pgvector  
**Purpose**: Vector embeddings for RAG  
**Protocol**: PostgreSQL native protocol  
**Configuration**:
- Tier: General Purpose
- vCores: 8
- Storage: 256GB SSD
- High Availability: Zone-redundant

---

### 5. Azure OpenAI ☁️
**Service**: Azure OpenAI Service  
**Purpose**: LLM inference for all agents  
**Protocol**: HTTPS/REST  
**Models**:
- GPT-4 (gpt-4-32k) for complex reasoning
- GPT-3.5-turbo for simple tasks
- text-embedding-ada-002 for embeddings

**Configuration**:
- Quota: 100K tokens/minute
- Deployment: Multi-region (East US, West Europe)

---

### 6. Content Filter (Azure AI) ☁️
**Service**: Azure AI Content Safety  
**Purpose**: Prompt injection detection, toxic content filtering  
**Protocol**: HTTPS/REST  
**Configuration**:
- Severity threshold: Medium
- Custom blocklist: Enabled

---

## 🌐 External APIs (Backend Systems)

### 1. Accounts API 🌐
**Type**: External Backend System  
**Protocol**: HTTPS/REST + OAuth 2.0  
**Endpoints**:
- GET /api/v1/accounts/{id}/balance
- GET /api/v1/accounts/{id}/transactions
- GET /api/v1/accounts/{id}/details

**Authentication**: OAuth 2.0 Client Credentials flow  
**SLA**: 99.9% availability, <200ms P95 latency

---

### 2. Cards API 🌐
**Type**: External Backend System  
**Protocol**: HTTPS/REST + OAuth 2.0  
**Endpoints**:
- GET /api/v1/cards/{id}
- GET /api/v1/cards/{id}/balance
- POST /api/v1/cards/applications
- GET /api/v1/cards/{id}/rewards

**Authentication**: OAuth 2.0 Client Credentials flow  
**SLA**: 99.9% availability, <300ms P95 latency

---

### 3. Loans API 🌐
**Type**: External Backend System  
**Protocol**: HTTPS/REST + OAuth 2.0  
**Endpoints**:
- POST /api/v1/loans/eligibility
- GET /api/v1/loans/products
- POST /api/v1/loans/applications
- GET /api/v1/loans/{id}

**Authentication**: OAuth 2.0 Client Credentials flow  
**SLA**: 99.9% availability, <400ms P95 latency

---

### 4. CRM/ServiceNow 🌐
**Type**: External SaaS Platform  
**Protocol**: HTTPS/REST + OAuth 2.0  
**Endpoints**:
- POST /api/now/table/incident (create case)
- GET /api/now/table/customer (get customer data)
- PATCH /api/now/table/incident/{id} (update case)

**Authentication**: OAuth 2.0 Authorization Code flow  
**SLA**: 99.5% availability per ServiceNow SLA

---

## 🏗️ AKS Cluster Configuration

### Cluster Specifications
- **Version**: Kubernetes 1.28
- **Node Pools**:
  - System pool: 3 nodes (Standard_D4s_v3)
  - User pool: 10 nodes (Standard_D8s_v3, autoscale 5-20)
- **Networking**: Azure CNI with Calico network policy
- **Service Mesh**: Istio 1.19
- **Ingress**: NGINX Ingress Controller with Azure Application Gateway

### Namespaces
- `agent-platform-prod`: Production workloads
- `agent-platform-monitoring`: Prometheus, Grafana
- `istio-system`: Istio control plane

### Security
- **Pod Security**: Restricted policy enforced
- **Network Policies**: Deny-all default, explicit allow rules
- **Secrets**: Azure Key Vault integration via CSI driver
- **RBAC**: Least privilege access per service account

---

## 📊 Deployment Summary

| Component Type | Count | Examples |
|----------------|-------|----------|
| **⭐ AKS Microservices** | 11 | API Gateway, Planner, Agents, MCP Tools |
| **☁️ Azure Managed Services** | 6 | Azure AD, Redis, Cosmos DB, PostgreSQL, OpenAI, Content Filter |
| **🌐 External APIs** | 4 | Accounts API, Cards API, Loans API, CRM |
| **Total Components** | 21 | Complete platform |

### Resource Allocation
- **Total vCPUs**: 45 (request), 90 (limit)
- **Total Memory**: 32GB (request), 64GB (limit)
- **Total Pods**: 35 (11 services × avg 3 replicas)

### Cost Estimate (Monthly)
- AKS cluster: $2,500
- Managed services: $3,800
- External API calls: $1,200
- **Total**: ~$7,500/month

---

## 🔄 Protocol Matrix

| From Component | To Component | Protocol | Port | Auth |
|----------------|--------------|----------|------|------|
| Customer | API Gateway ⭐ | HTTPS/REST | 443 | JWT |
| API Gateway ⭐ | Azure AD ☁️ | HTTPS (OAuth) | 443 | Client credentials |
| API Gateway ⭐ | Planner ⭐ | HTTP/REST | 8080 | mTLS |
| Planner ⭐ | Memory Manager ⭐ | HTTP/REST | 8080 | mTLS |
| Planner ⭐ | Azure OpenAI ☁️ | HTTPS/REST | 443 | API key |
| Tool Selector ⭐ | Executor ⭐ | HTTP/REST | 8080 | mTLS |
| Executor ⭐ | Card Agent ⭐ | gRPC | 9090 | mTLS |
| Executor ⭐ | Loan Agent ⭐ | gRPC | 9090 | mTLS |
| Executor ⭐ | Wealth Agent ⭐ | gRPC | 9090 | mTLS |
| Card Agent ⭐ | Azure OpenAI ☁️ | HTTPS/REST | 443 | API key |
| Card Agent ⭐ | MCP Tools ⭐ | HTTP/REST | 8080 | mTLS |
| Card Agent ⭐ | Redis ☁️ | Redis Pub/Sub | 6379 | Password |
| Loan Agent ⭐ | RAG Engine ⭐ | HTTP/REST | 8080 | mTLS |
| Wealth Agent ⭐ | RAG Engine ⭐ | HTTP/REST | 8080 | mTLS |
| MCP Tools ⭐ | Accounts API 🌐 | HTTPS + OAuth 2.0 | 443 | OAuth 2.0 |
| MCP Tools ⭐ | Cards API 🌐 | HTTPS + OAuth 2.0 | 443 | OAuth 2.0 |
| MCP Tools ⭐ | Loans API 🌐 | HTTPS + OAuth 2.0 | 443 | OAuth 2.0 |
| MCP Tools ⭐ | CRM 🌐 | HTTPS + OAuth 2.0 | 443 | OAuth 2.0 |
| Memory Manager ⭐ | Cosmos DB ☁️ | MongoDB Wire | 27017 | Connection string |
| Memory Manager ⭐ | Redis ☁️ | Redis RESP3 | 6379 | Password |
| RAG Engine ⭐ | Vector DB ☁️ | PostgreSQL | 5432 | Username/password |

**Key Protocols:**
- **mTLS**: Mutual TLS for inter-service communication within AKS
- **gRPC**: High-performance RPC for Executor ↔ Agents
- **Redis Pub/Sub**: Event-driven agent coordination
- **OAuth 2.0**: Secure API authentication for external systems

---

## 🎯 Summary

**AKS Microservices (⭐)**: 11 containerized services running in Kubernetes
- API Gateway, Planner, Tool Selector, Executor, Critic
- Card Agent, Loan Agent, Wealth Agent
- Memory Manager, RAG Engine, MCP Tools

**Azure Managed Services (☁️)**: 6 PaaS services
- Azure AD, Redis, Cosmos DB, PostgreSQL, OpenAI, Content Filter

**External APIs (🌐)**: 4 backend systems
- Accounts API, Cards API, Loans API, CRM/ServiceNow

**All components are clearly labeled in the visualizer with ⭐/☁️/🌐 badges!**
