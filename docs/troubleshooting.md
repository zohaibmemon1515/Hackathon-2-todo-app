# Troubleshooting Guide for Todo Chatbot Kubernetes Deployment

## Common Issues and Solutions

### 1. Minikube Not Starting
**Problem**: Minikube fails to start
**Solution**:
- Check if virtualization is enabled in BIOS
- Try different drivers: `minikube start --driver=docker`
- Increase allocated resources: `minikube start --memory=4096 --cpus=2`

### 2. Pod Stuck in Pending State
**Problem**: Pods remain in "Pending" status
**Solution**:
- Check available resources: `kubectl describe nodes`
- Verify resource requests in deployment: `kubectl describe deployment <deployment-name>`
- Check if there are taints on nodes preventing scheduling

### 3. Image Pull Errors
**Problem**: Pods fail with "ImagePullBackOff" or "ErrImagePull"
**Solution**:
- Ensure Docker images are built and available
- For Minikube, use: `minikube image load <image-name>`
- Check image names in values.yaml match built images

### 4. Service Connectivity Issues
**Problem**: Frontend cannot reach backend services
**Solution**:
- Verify service names match what's referenced in frontend: `kubectl get svc`
- Check if services are exposing correct ports
- Verify environment variables in frontend deployment

### 5. Ingress Not Working
**Problem**: Cannot access application via ingress
**Solution**:
- Enable ingress addon: `minikube addons enable ingress`
- Check ingress controller status: `kubectl get pods -n ingress-nginx`
- Verify ingress configuration: `kubectl describe ingress <ingress-name>`

### 6. Helm Installation Failures
**Problem**: Helm install/upgrade fails
**Solution**:
- Check chart dependencies: `helm dependency update`
- Verify chart syntax: `helm lint`
- Check for existing releases: `helm list`

### 7. Resource Constraints
**Problem**: Pods evicted due to resource pressure
**Solution**:
- Adjust resource limits and requests in values.yaml
- Increase Minikube resources
- Check current usage: `kubectl top nodes`

### 8. Configuration Issues
**Problem**: Application not behaving as expected
**Solution**:
- Verify environment variables: `kubectl describe pod <pod-name>`
- Check ConfigMaps: `kubectl get configmaps`
- Verify mounted volumes: `kubectl describe pod <pod-name>`

## Diagnostic Commands

### General Health Check
```bash
kubectl get pods,svc,ingress,deployments -o wide
```

### Pod Diagnostics
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs
```

### Service Diagnostics
```bash
kubectl describe svc <service-name>
kubectl get endpoints <service-name>
```

### Deployment Diagnostics
```bash
kubectl describe deployment <deployment-name>
kubectl rollout status deployment/<deployment-name>
```

## Rollback Procedures

### Rollback Helm Release
```bash
helm list  # Check revision history
helm rollback <release-name> <revision-number>
```

### Scale Down/Up
```bash
kubectl scale deployment <deployment-name> --replicas=0  # Scale down
kubectl scale deployment <deployment-name> --replicas=<desired-count>  # Scale up
```

## Performance Optimization

### Resource Recommendations
- Frontend: 128Mi-256Mi memory, 100m-200m CPU
- Backend: 256Mi-512Mi memory, 200m-500m CPU
- Adjust based on actual usage patterns

### Monitoring Commands
```bash
kubectl top pods  # Resource usage
kubectl get hpa   # Horizontal Pod Autoscaler status (if configured)
```