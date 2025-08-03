# Kubernetes Deployment Guide

## Prerequisites
- Docker installed
- Kubernetes cluster (local or cloud)
- kubectl configured
- ScraperAPI key

## Deployment Steps

1. Build and push the Docker image:
```bash
# Build the image
docker build -t fashion-deal-recommender:latest .

# If using a remote registry:
docker tag fashion-deal-recommender:latest your-registry/fashion-deal-recommender:latest
docker push your-registry/fashion-deal-recommender:latest
```

2. Create the ScraperAPI secret:
```bash
# First, base64 encode your API key
echo -n 'your-api-key' | base64

# Update the secret.yaml file with the encoded key
# Then create the secret
kubectl apply -f k8s/secret.yaml
```

3. Apply the Kubernetes manifests:
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

4. Verify the deployment:
```bash
kubectl get pods
kubectl get services
```

## Monitoring

Check pod status:
```bash
kubectl get pods
kubectl logs -f deployment/fashion-deal-recommender
```

## Scaling

Scale the deployment:
```bash
kubectl scale deployment fashion-deal-recommender --replicas=3
```

## Configuration

The application uses:
- ConfigMap for general configuration
- Secret for API key storage
- Service type LoadBalancer for external access
- Resource limits and health checks configured in deployment

## Cleanup

To remove the deployment:
```bash
kubectl delete -f k8s/
```
