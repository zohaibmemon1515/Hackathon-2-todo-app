# Cloud Native Todo Chatbot 🤖☸️

A cloud-native Todo Chatbot application built using a **Spec-Driven Development** approach and deployed locally on **Kubernetes (Minikube)** using **Helm Charts**, with **AI-assisted DevOps tools** like Docker AI (Gordon), kubectl-ai, and Kagent.

This project is developed as part of **Hackathon II – Spec-Driven Development**.

---

## 📌 Project Overview

The Todo Chatbot allows users to manage tasks via a conversational interface.  
The application follows modern **cloud-native principles**, is containerized using Docker, and orchestrated using Kubernetes.

The development strictly follows the **Agentic Dev Stack workflow**:

> **Write Spec → Generate Plan → Break into Tasks → Implement via AI Agents**  
> ❌ No manual coding

---

## 🧩 Project Phases

### ✅ Phase III – Application Development
- Developed Todo Chatbot frontend and backend
- Implemented basic chatbot functionality
- Exposed APIs for task creation, listing, and deletion

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
