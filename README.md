# Kubernetes Microservices Demo

A demonstration project showcasing microservice architecture with three interconnected FastAPI services, a KrakenD API gateway, Docker Compose orchestration, and Kubernetes deployment.

## Architecture Overview

```
                        ┌──────────────┐
                        │   KrakenD    │
                        │ API Gateway  │
                        │  (port 8090) │
                        └──────┬───────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
       ┌──────▼──────┐ ┌──────▼──────┐ ┌───────▼─────┐
       │  Service A   │ │  Service B   │ │  Service C   │
       │ (port 8005)  │ │ (port 8006)  │ │ (port 8007)  │
       └──────────────┘ └──────────────┘ └──────────────┘
              ▲                ▲                ▲
              └────────────────┴────────────────┘
                  (call each other via HTTP)
```

- **Service A** (port 8005) — can call Service B and Service C
- **Service B** (port 8006) — can call Service A and Service C
- **Service C** (port 8007) — can call Service A and Service B
- **KrakenD API Gateway** (port 8090) — single entry point that routes requests to all services

Each service is a Python FastAPI app that communicates with the others using async HTTP (httpx).

## Prerequisites

Before you start, make sure you have the following installed on your machine:

| Tool | Purpose | Install Guide |
|------|---------|---------------|
| **Docker** | Build and run container images | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |
| **Docker Compose** | Orchestrate multi-container setup locally | Included with Docker Desktop |
| **kubectl** | Interact with Kubernetes clusters | [kubernetes.io/docs/tasks/tools](https://kubernetes.io/docs/tasks/tools/) |
| **Minikube** (or any K8s cluster) | Run a local Kubernetes cluster | [minikube.sigs.k8s.io/docs/start](https://minikube.sigs.k8s.io/docs/start/) |
| **Python 3.11+** | Run services locally without Docker (optional) | [python.org/downloads](https://www.python.org/downloads/) |

## Project Structure

```
kubernetes-microservices-demo/
├── docker-compose.yml              # Docker Compose orchestration
├── api-gateway/
│   ├── krakend-local/              # KrakenD config for local/Docker development
│   │   ├── docker-compose.yml
│   │   └── krakend.json
│   └── krakend-prod/               # KrakenD config for production/Kubernetes
│       └── krakend.json
├── services/
│   ├── service-a/                  # Microservice A (FastAPI, port 8005)
│   ├── service-b/                  # Microservice B (FastAPI, port 8006)
│   ├── service-c/                  # Microservice C (FastAPI, port 8007)
│   └── docs/                       # Services documentation
└── docs/
    ├── kubernetes/                 # Kubernetes troubleshooting commands
    ├── deployment/                 # Deployment guides
    └── project-setup/              # Setup documentation
```

## Getting Started

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/kubernetes-microservices-demo.git
cd kubernetes-microservices-demo
```

### Step 2: Set Up Environment Variables

Each service has a `.env.example` file. Copy it to `.env`:

```bash
cp services/service-a/.env.example services/service-a/.env
cp services/service-b/.env.example services/service-b/.env
cp services/service-c/.env.example services/service-c/.env
```

Default values point to `localhost` which works for local development without Docker.

---

## Running with Docker Compose (Recommended)

This is the easiest way to run everything together.

### Step 1: Build and Start All Services

```bash
docker-compose up --build
```

This starts all four containers (Service A, B, C, and KrakenD) on a shared network (`microservices-network`).

### Step 2: Verify Services Are Running

```bash
docker-compose ps
```

All services should show as "healthy" after ~30 seconds.

### Step 3: Test the Services

Through the API Gateway (single entry point):
```bash
# Service A root
curl http://localhost:8090/api/v1/service-a/

# Service A calls Service B
curl http://localhost:8090/api/v1/service-a/services/call-service-b

# Service B health check
curl http://localhost:8090/api/v1/service-b/health

# Service C calls Service A
curl http://localhost:8090/api/v1/service-c/services/call-service-a
```

Or directly to individual services:
```bash
curl http://localhost:8005/api/v1/         # Service A
curl http://localhost:8006/api/v1/         # Service B
curl http://localhost:8007/api/v1/         # Service C
```

### Step 4: View Swagger Documentation

Each service has auto-generated API docs:
- Service A: http://localhost:8005/docs
- Service B: http://localhost:8006/docs
- Service C: http://localhost:8007/docs

### Step 5: Stop All Services

```bash
docker-compose down
```

---

## Running Locally Without Docker (for development)

If you want to run services directly on your machine for faster development iteration.

### Step 1: Create Virtual Environments and Install Dependencies

```bash
# Service A
cd services/service-a
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Repeat for service-b and service-c
```

### Step 2: Start Each Service (in separate terminals)

```bash
# Terminal 1 — Service A
cd services/service-a
uvicorn service_a.main:app --host 0.0.0.0 --port 8005 --reload

# Terminal 2 — Service B
cd services/service-b
uvicorn service_b.main:app --host 0.0.0.0 --port 8006 --reload

# Terminal 3 — Service C
cd services/service-c
uvicorn service_c.main:app --host 0.0.0.0 --port 8007 --reload
```

The `--reload` flag enables auto-restart on code changes.

---

## Deploying to Kubernetes

### Step 1: Start a Local Kubernetes Cluster

Using Minikube:
```bash
minikube start
```

Verify the cluster is running:
```bash
kubectl cluster-info
kubectl get nodes
```

### Step 2: Build Docker Images

If using Minikube, point your Docker CLI to Minikube's Docker daemon so images are available inside the cluster:

```bash
eval $(minikube docker-env)
```

Then build the images:
```bash
docker build -t service-a:latest ./services/service-a
docker build -t service-b:latest ./services/service-b
docker build -t service-c:latest ./services/service-c
```

### Step 3: Create a Namespace

```bash
kubectl create namespace microservices-demo
```

### Step 4: Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/ -n microservices-demo
```

### Step 5: Verify the Deployment

```bash
# Check all pods are running
kubectl -n microservices-demo get pods

# Check services are created
kubectl -n microservices-demo get svc

# Check deployments
kubectl -n microservices-demo get deployments
```

Wait until all pods show `STATUS: Running` and `READY: 1/1`.

### Step 6: Access the Services

Using Minikube, you can access services via port-forward:
```bash
# Forward Service A to localhost:8005
kubectl -n microservices-demo port-forward svc/service-a 8005:8005

# Or forward the API Gateway
kubectl -n microservices-demo port-forward svc/krakend 8090:8080
```

---

## API Endpoints Reference

Each service exposes the following endpoints:

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/` | Service info (name, version) |
| `GET /api/v1/health` | Health check |
| `GET /api/v1/services/call-service-{a\|b\|c}` | Call another service |
| `GET /docs` | Swagger UI documentation |

Through the KrakenD API Gateway (port 8090):

| Endpoint | Routes To |
|----------|-----------|
| `GET /api/v1/service-a/*` | Service A |
| `GET /api/v1/service-b/*` | Service B |
| `GET /api/v1/service-c/*` | Service C |

---

## Troubleshooting

### Docker Compose Issues

```bash
# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs service-a

# Rebuild everything from scratch
docker-compose down
docker-compose up --build --force-recreate
```

### Kubernetes Issues

```bash
# Check pod status
kubectl -n microservices-demo get pods

# View pod logs
kubectl -n microservices-demo logs <podname>

# Describe a pod for detailed info and events
kubectl -n microservices-demo describe pod <podname>

# Shell into a running container
kubectl -n microservices-demo exec -it <podname> -- /bin/sh

# Check events for errors
kubectl -n microservices-demo get events --sort-by='.lastTimestamp'
```

For a full list of useful Kubernetes troubleshooting commands, see [Essential Statements for Problem Solving](docs/kubernetes/Essential_statements_for_problem_solving.md).

---

## Tech Stack

| Technology | Role |
|------------|------|
| **Python 3.11** | Service runtime |
| **FastAPI** | Web framework |
| **Uvicorn** | ASGI server |
| **httpx** | Async HTTP client for service-to-service calls |
| **KrakenD** | API Gateway |
| **Docker** | Containerization |
| **Docker Compose** | Local multi-container orchestration |
| **Kubernetes** | Production container orchestration |
