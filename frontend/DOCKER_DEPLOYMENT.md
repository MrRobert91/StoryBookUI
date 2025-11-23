# Docker Deployment Guide

## Quick Start (Local)

### Using Docker Compose (Recommended)
\`\`\`bash
# 1. Set up environment
cp .env.docker .env.local
# Edit .env.local with your Supabase and FastAPI URLs

# 2. Build and run
docker-compose up -d

# 3. Access app
# http://localhost:3000
\`\`\`

### Using Docker CLI
\`\`\`bash
# Build image
docker build -t cuentee:latest .

# Run container
docker run -d \
  -p 3000:3000 \
  -e NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co \
  -e NEXT_PUBLIC_SUPABASE_ANON_KEY=your-key \
  -e NEXT_PUBLIC_FASTAPI_URL=https://your-api.com \
  --name cuentee \
  cuentee:latest

# View logs
docker logs -f cuentee
\`\`\`

## Production Deployment

### Environment Variables
Set these in your cloud provider:
- \`NEXT_PUBLIC_SUPABASE_URL\` - Supabase project URL
- \`NEXT_PUBLIC_SUPABASE_ANON_KEY\` - Public anon key
- \`SUPABASE_SERVICE_ROLE_KEY\` - Service role key (sensitive)
- \`SUPABASE_JWT_SECRET\` - JWT secret (sensitive)
- \`NEXT_PUBLIC_FASTAPI_URL\` - Backend API URL
- Any payment/AI integration keys

### AWS ECR Deployment
\`\`\`bash
# Create ECR repository
aws ecr create-repository --repository-name cuentee

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag cuentee:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/cuentee:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/cuentee:latest

# Deploy on ECS/Fargate or EC2
\`\`\`

### Google Cloud Run
\`\`\`bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cuentee

# Deploy
gcloud run deploy cuentee \
  --image gcr.io/YOUR_PROJECT_ID/cuentee \
  --platform managed \
  --region us-central1 \
  --set-env-vars "NEXT_PUBLIC_SUPABASE_URL=...,NEXT_PUBLIC_FASTAPI_URL=..."
\`\`\`

### Azure Container Instances
\`\`\`bash
# Create registry
az acr create --resource-group myResourceGroup --name cuenteeregistry --sku Basic

# Build and push
az acr build --registry cuenteeregistry --image cuentee:latest .

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name cuentee \
  --image cuenteeregistry.azurecr.io/cuentee:latest \
  --environment-variables NEXT_PUBLIC_SUPABASE_URL=... \
  --ports 3000 \
  --cpu 1 --memory 1
\`\`\`

### Docker Hub
\`\`\`bash
# Login
docker login

# Tag
docker tag cuentee:latest yourusername/cuentee:latest

# Push
docker push yourusername/cuentee:latest
\`\`\`

### Kubernetes
\`\`\`bash
# Create deployment
kubectl create deployment cuentee --image=your-registry/cuentee:latest
kubectl set env deployment/cuentee NEXT_PUBLIC_SUPABASE_URL=...
kubectl expose deployment cuentee --type=LoadBalancer --port=80 --target-port=3000

# Or use YAML manifest
kubectl apply -f k8s-deployment.yaml
\`\`\`

## Health Checks & Monitoring

The Dockerfile includes a health check that pings the application every 30 seconds. View health status:

\`\`\`bash
docker ps --filter "name=cuentee"
\`\`\`

## Troubleshooting

### Container won't start
\`\`\`bash
docker logs cuentee
# Check for environment variable issues
\`\`\`

### Build fails
\`\`\`bash
# Check Next.js build
docker build --progress=plain .
\`\`\`

### Connection issues
- Verify environment variables are set correctly
- Check Supabase and FastAPI URLs are accessible
- Test with: \`curl http://localhost:3000\`

## Performance Optimization

- Image is ~600MB (uses Alpine Linux for minimal size)
- Multi-stage build reduces final image size
- Node 20 Alpine for security and performance
- Production-optimized Next.js build

## Security

- Non-root user (nextjs) for container execution
- Alpine Linux base image (minimal attack surface)
- .dockerignore prevents leaking sensitive files
- No secrets in image layers
- Environment variables for sensitive data
