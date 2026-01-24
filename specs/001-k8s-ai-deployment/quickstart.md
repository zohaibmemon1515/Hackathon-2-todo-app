# Quickstart Guide: Cloud-Native Todo Chatbot – Phase IV (Local Kubernetes Deployment)

## Prerequisites

- Docker Desktop running
- Minikube installed and configured
- kubectl installed and configured
- Helm installed
- AI-assisted tools: Docker AI (Gordon), kubectl-ai, Kagent

## Setup Instructions

### 1. Environment Preparation
```bash
# Start Minikube cluster
minikube start

# Verify cluster is accessible
kubectl cluster-info

# Verify Helm is available
helm version
```

### 2. AI-Assisted Containerization
```bash
# Use Docker AI to generate Dockerfiles for frontend
# (Command to be determined by Docker AI agent)

# Use Docker AI to generate Dockerfiles for backend
# (Command to be determined by Docker AI agent)

# Build Docker images using generated Dockerfiles
docker build -t todo-frontend ./apps/frontend
docker build -t todo-backend ./apps/backend
```

### 3. Deploy with Helm
```bash
# Navigate to Helm chart directory
cd k8s/helm-chart

# Install the Helm chart
helm install todo-chatbot .

# Verify deployment
kubectl get pods
kubectl get services
```

### 4. Access the Application
```bash
# Get the frontend service URL
minikube service frontend-service --url

# Or access via ingress if configured
minikube tunnel  # In separate terminal
# Then access via configured ingress hostname
```

### 5. Validation Commands
```bash
# Check all pods are running
kubectl get pods

# Check services are available
kubectl get services

# Verify replica counts
kubectl get deployments

# Check application logs
kubectl logs -l app=frontend
kubectl logs -l app=backend
```

## Troubleshooting with AI Tools

### Using kubectl-ai
```bash
# Ask kubectl-ai to diagnose issues
kubectl-ai "diagnose why pods are not starting"

# Get AI recommendations for scaling
kubectl-ai "scale frontend deployment to 3 replicas"
```

### Using Kagent
```bash
# Analyze cluster health
kagent analyze

# Get optimization recommendations
kagent optimize
```

## Clean Up
```bash
# Uninstall Helm release
helm uninstall todo-chatbot

# Stop Minikube
minikube stop
```