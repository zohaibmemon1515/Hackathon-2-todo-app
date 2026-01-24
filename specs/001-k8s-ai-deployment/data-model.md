# Data Model: Cloud-Native Todo Chatbot – Phase IV (Local Kubernetes Deployment)

## Kubernetes Resources

### Deployment Entities

**Frontend Deployment**
- **Name**: frontend-deployment
- **Replicas**: 2 (configurable via Helm values)
- **Container Image**: todo-frontend (to be built from /apps/frontend)
- **Ports**: 3000 (exposed to service)
- **Environment Variables**: BACKEND_SERVICE_URL (internal service reference)

**Backend Deployment**
- **Name**: backend-deployment
- **Replicas**: 1 (configurable via Helm values)
- **Container Image**: todo-backend (to be built from /apps/backend)
- **Ports**: 8000 (exposed to service)
- **Environment Variables**: Database connection details (if needed)

### Service Entities

**Frontend Service**
- **Name**: frontend-service
- **Type**: ClusterIP or LoadBalancer (configurable)
- **Port**: 80 (external), maps to container port 3000
- **Selector**: Matches frontend deployment labels

**Backend Service**
- **Name**: backend-service
- **Type**: ClusterIP
- **Port**: 80 (external), maps to container port 8000
- **Selector**: Matches backend deployment labels

### Ingress Entity

**Application Ingress**
- **Name**: todo-chatbot-ingress
- **Host**: localhost or minikube IP
- **Path**: / -> frontend-service
- **Rules**: Routes traffic to frontend service

### ConfigMap Entity

**Application Configuration**
- **Name**: todo-chatbot-config
- **Data**:
  - FRONTEND_ENV: development
  - BACKEND_URL: http://backend-service:80

## Helm Chart Structure

### Chart Metadata
- **Name**: todo-chatbot
- **Version**: 0.1.0
- **AppVersion**: 1.0.0

### Values Parameters
- **frontend.replicaCount**: Number of frontend replicas (default: 2)
- **backend.replicaCount**: Number of backend replicas (default: 1)
- **frontend.image.repository**: Frontend image repository
- **backend.image.repository**: Backend image repository
- **frontend.service.type**: Frontend service type
- **backend.service.type**: Backend service type
- **ingress.enabled**: Whether to enable ingress
- **ingress.hosts**: Hosts for ingress routing

## Docker Image Specifications

### Frontend Image
- **Base Image**: NodeJS LTS or Alpine-based
- **Build Context**: /apps/frontend
- **Exposed Port**: 3000
- **Health Check**: HTTP GET on /health endpoint

### Backend Image
- **Base Image**: Python 3.11+ or Alpine-based
- **Build Context**: /apps/backend
- **Exposed Port**: 8000
- **Health Check**: HTTP GET on /health endpoint