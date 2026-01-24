# Ollama Docker Setup Guide

## Overview
This guide shows you how to run Ollama in Docker containers for isolated, reproducible LLM deployments.

## Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)
- At least 8GB RAM available
- 10GB+ free disk space

---

## Method 1: Basic Docker Run

### Pull and Run Ollama Container

```bash
# Pull the official Ollama image
docker pull ollama/ollama

# Run Ollama container
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama

# Check if it's running
docker ps
```

### Pull a Model Inside Container

```bash
# Execute command inside the container
docker exec -it ollama ollama pull llama2

# List available models
docker exec -it ollama ollama list

# Run model interactively
docker exec -it ollama ollama run llama2
```

### Test the API

```bash
# From your host machine
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

---

## Method 2: Docker Compose (Recommended)

### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    environment:
      - OLLAMA_HOST=0.0.0.0
    # Optional: GPU support (requires nvidia-docker)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]

volumes:
  ollama_data:
    driver: local
```

### Start the Service

```bash
# Start Ollama
docker-compose up -d

# View logs
docker-compose logs -f ollama

# Pull a model
docker-compose exec ollama ollama pull llama2

# Stop the service
docker-compose down

# Stop and remove volumes (deletes models)
docker-compose down -v
```

---

## Method 3: Custom Dockerfile with Pre-loaded Models

### Create `Dockerfile`

```dockerfile
FROM ollama/ollama:latest

# Set working directory
WORKDIR /app

# Copy initialization script
COPY init-models.sh /app/init-models.sh
RUN chmod +x /app/init-models.sh

# Expose Ollama port
EXPOSE 11434

# Start Ollama and pull models
CMD ["/app/init-models.sh"]
```

### Create `init-models.sh`

```bash
#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start
sleep 5

# Pull models
echo "Pulling llama2..."
ollama pull llama2

echo "Pulling mistral..."
ollama pull mistral

echo "Models ready!"

# Keep container running
wait
```

### Build and Run

```bash
# Build custom image
docker build -t ollama-custom .

# Run container
docker run -d \
  --name ollama-custom \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama-custom

# Check logs
docker logs -f ollama-custom
```

---

## Method 4: Docker Compose with Multiple Services

### Advanced `docker-compose.yml`

```yaml
version: '3.8'

services:
  # Ollama LLM Service
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    networks:
      - llm-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Python API Service (FastAPI)
  api:
    build: ./api
    container_name: llm-api
    ports:
      - "8000:8000"
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    networks:
      - llm-network
    restart: unless-stopped

  # Optional: Web UI
  web:
    image: nginx:alpine
    container_name: llm-web
    ports:
      - "80:80"
    volumes:
      - ./web:/usr/share/nginx/html
    depends_on:
      - api
    networks:
      - llm-network
    restart: unless-stopped

networks:
  llm-network:
    driver: bridge

volumes:
  ollama_data:
    driver: local
```

---

## GPU Support (NVIDIA)

### Prerequisites
- NVIDIA GPU
- NVIDIA Docker runtime installed

### Install NVIDIA Container Toolkit

```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Docker Compose with GPU

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-gpu
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  ollama_data:
```

### Run with GPU

```bash
# Using docker run
docker run -d \
  --gpus all \
  --name ollama-gpu \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama

# Using docker-compose
docker-compose up -d
```

---

## Python Client for Dockerized Ollama

### `ollama_client.py`

```python
import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model, prompt, stream=False):
        """Generate response from Ollama."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            raise Exception(f"Error: {response.status_code}")
    
    def chat(self, model, messages):
        """Chat completion."""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            raise Exception(f"Error: {response.status_code}")

# Usage
if __name__ == "__main__":
    client = OllamaClient()
    
    # Simple generation
    response = client.generate("llama2", "What is Docker?")
    print(response)
    
    # Chat
    messages = [
        {"role": "user", "content": "Explain containers"}
    ]
    response = client.chat("llama2", messages)
    print(response)
```

---

## Useful Docker Commands

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View logs
docker logs ollama
docker logs -f ollama  # Follow logs

# Execute command in container
docker exec -it ollama bash
docker exec -it ollama ollama list

# Stop container
docker stop ollama

# Start container
docker start ollama

# Remove container
docker rm ollama

# Remove image
docker rmi ollama/ollama

# View disk usage
docker system df

# Clean up unused resources
docker system prune -a

# View volume contents
docker volume inspect ollama_data
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs ollama

# Check if port is already in use
lsof -i :11434

# Remove and recreate
docker-compose down
docker-compose up -d
```

### Model Download Fails

```bash
# Check disk space
df -h

# Check container logs
docker logs ollama

# Manually pull model
docker exec -it ollama ollama pull llama2
```

### API Not Responding

```bash
# Check if service is running
curl http://localhost:11434/api/tags

# Restart container
docker restart ollama

# Check network
docker network inspect bridge
```

### Out of Memory

```bash
# Increase Docker memory limit (Docker Desktop)
# Settings > Resources > Memory

# Or use smaller models
docker exec -it ollama ollama pull phi  # 2.7B model
```

---

## Production Considerations

### 1. Resource Limits

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

### 2. Persistent Storage

```yaml
volumes:
  ollama_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/to/persistent/storage
```

### 3. Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 4. Logging

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 5. Security

```yaml
# Don't expose to public internet without authentication
ports:
  - "127.0.0.1:11434:11434"  # Only localhost

# Use secrets for sensitive data
secrets:
  api_key:
    file: ./secrets/api_key.txt
```

---

## Next Steps

1. ✅ Set up Docker Compose
2. ✅ Pull required models
3. ✅ Test API endpoints
4. ✅ Integrate with Python
5. ✅ Build FastAPI wrapper
6. ✅ Deploy to production

## Resources

- [Ollama Docker Hub](https://hub.docker.com/r/ollama/ollama)
- [Ollama Documentation](https://ollama.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
