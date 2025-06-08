# fraud_detection

## Deployment

```bash
doctl kubernetes cluster kubeconfig save aids

# Build and tag your Docker image
docker build --platform linux/amd64 --provenance false -t registry.digitalocean.com/grifflesctf2025/fraud_detection:latest .

# Push the image to the registry
docker push registry.digitalocean.com/grifflesctf2025/fraud_detection:latest

# Apply the Kubernetes manifest
doctl registry kubernetes-manifest | kubectl apply -f -

# Apply the deployment
kubectl apply -f k8s/deployment.yml

# Check for external IPs
kubectl get services fraud_detection
```
