# Cloud Native Todo Chatbot 🤖☸️

A cloud-native Todo Chatbot application built using a **Spec-Driven Development** approach and deployed locally on **Kubernetes (Minikube)** using **Helm Charts**, with **AI-assisted DevOps tools** like Docker AI (Gordon), kubectl-ai, and Kagent.

This project is developed as part of **Hackathon II – Spec-Driven Development**.

---

## 📌 Project Overview

The Todo Chatbot allows users to manage tasks via a conversational interface.  
The application is designed following modern **cloud-native principles**, containerized using Docker, and orchestrated using Kubernetes.

The development strictly follows the **Agentic Dev Stack workflow**:

> **Write Spec → Generate Plan → Break into Tasks → Implement via AI Agents**  
> ❌ No manual coding

---

## 🧩 Project Phases

### ✅ Phase III – Application Development
- Developed Todo Chatbot frontend and backend
- Basic chatbot functionality implemented
- APIs exposed for task creation, listing, and deletion

### ✅ Phase IV – Cloud-Native Deployment (Current Phase)
- Containerized frontend and backend using **Docker AI Agent (Gordon)**
- Created **Helm Charts** for Kubernetes deployment
- Deployed application on **Minikube**
- Used **kubectl-ai** and **Kagent** for AI-assisted Kubernetes operations

---

## 🛠️ Technology Stack

| Layer | Technology |
|-----|------------|
| Frontend | Phase III Todo Frontend |
| Backend | Phase III Todo Backend |
| Containerization | Docker, Docker Desktop |
| AI Docker Ops | Docker AI Agent (Gordon) |
| Orchestration | Kubernetes (Minikube) |
| Package Manager | Helm |
| AI Kubernetes Ops | kubectl-ai, Kagent |
| Dev Approach | Spec-Driven Development |

---

## 📂 Repository Structure

```text
apps/
├── backend/
│   └── Dockerfile
├── frontend/
│   └── Dockerfile
└── helm/
    └── todo-app/
        ├── Chart.yaml
        ├── values.yaml
        ├── .helmignore
        └── templates/
            ├── backend-deployment.yaml
            ├── backend-service.yaml
            ├── frontend-deployment.yaml
            └── frontend-service.yaml


🐳 Containerization (Docker AI – Gordon)

Frontend and backend applications were containerized using Docker Desktop with Docker AI Agent (Gordon).

Example AI command:

docker ai "What can you do?"


Docker AI assisted in:

Image creation

Container optimization

Docker best-practice suggestions

☸️ Kubernetes Setup (Minikube)

Local Kubernetes cluster created using Minikube

Docker Desktop used as container runtime

Cluster verified using:

kubectl get nodes

📦 Helm Chart Deployment

Helm was used to package and deploy the application.

Install Helm Chart
helm install todo-app ./apps/helm/todo-app

Verify Resources
kubectl get pods
kubectl get services


Expected running pods:

todo-backend

todo-frontend

🤖 AI-Assisted Kubernetes Operations
Using kubectl-ai
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to handle more load"
kubectl-ai "check why the pods are failing"

Using Kagent
kagent "analyze the cluster health"
kagent "optimize resource allocation"


These tools provided intelligent insights and automation for Kubernetes management.

📊 Deployment Status
Component	Status
Minikube	Running
Pods	Running
Services	Active
Helm Release	Deployed Successfully
🧪 Validation
kubectl get pods
kubectl describe pod <pod-name>


All pods are running without restarts.

📚 Learning Outcomes

Hands-on experience with cloud-native architecture

Practical usage of Helm Charts

Exposure to AI-driven DevOps tools

Understanding Spec-Driven Infrastructure Automation

🔮 Future Enhancements

Add Ingress controller

Enable Horizontal Pod Autoscaling (HPA)

Deploy on managed Kubernetes (EKS/GKE/AKS)

Integrate monitoring (Prometheus + Grafana)

🏁 Conclusion

This phase demonstrates how Spec-Driven Development and AI Agents can be effectively used for cloud-native infrastructure automation, enabling faster, smarter, and more reliable deployments.

👤 Author

Zohaib Memon
Hackathon II – Cloud Native & AI DevOps


---

## ✅ Last step (IMPORTANT)

Save ke baad ye commands chalana mat bhoolna:

```bash
git add README.md
git commit -m "Add complete README for Phase IV Kubernetes deployment"
git push
