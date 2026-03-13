# Kubernetes Microservices Demo - Services

## Project Structure

```
services/
├── service-a/
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   └── service_a/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   └── v1/
│       │       └── routers/
│       │           ├── health.py
│       │           └── services.py
│       └── core/
│           └── config.py
├── service-b/
│   └── ... (same structure)
└── service-c/
    └── ... (same structure)
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| Service A | 8005 | Microservice A API |
| Service B | 8006 | Microservice B API |
| Service C | 8007 | Microservice C API |

## API Endpoints

Each service exposes the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/` | GET | Root endpoint |
| `/api/v1/health` | GET | Health check |
| `/api/v1/services/call-service-{x}` | GET | Call another service |
| `/docs` | GET | Swagger UI documentation |
| `/api/openapi.json` | GET | OpenAPI schema |

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kubernetes-microservices-demo.git
cd kubernetes-microservices-demo
```

2. Set up each service:
```bash
# Service A
cd services/service-a
cp .env.example .env
pip install -r requirements.txt

# Service B
cd ../service-b
cp .env.example .env
pip install -r requirements.txt

# Service C
cd ../service-c
cp .env.example .env
pip install -r requirements.txt
```

### Running the Services

Run each service in a separate terminal:

```bash
# Terminal 1 - Service A
cd services/service-a
uvicorn service_a.main:app --reload --port 8005

# Terminal 2 - Service B
cd services/service-b
uvicorn service_b.main:app --reload --port 8006

# Terminal 3 - Service C
cd services/service-c
uvicorn service_c.main:app --reload --port 8007
```

### Testing the Services

Once all services are running, you can test them:

```bash
# Test Service A
curl http://localhost:8005/api/v1/
curl http://localhost:8005/api/v1/health

# Call Service B from Service A
curl http://localhost:8005/api/v1/services/call-service-b

# Call Service C from Service A
curl http://localhost:8005/api/v1/services/call-service-c
```

Or visit the Swagger UI:
- Service A: http://localhost:8005/docs
- Service B: http://localhost:8006/docs
- Service C: http://localhost:8007/docs

## Environment Variables

Each service uses the following environment variables:

### Service A
| Variable | Default | Description |
|----------|---------|-------------|
| SERVICE_B_URL | http://localhost:8006 | URL of Service B |
| SERVICE_C_URL | http://localhost:8007 | URL of Service C |

### Service B
| Variable | Default | Description |
|----------|---------|-------------|
| SERVICE_A_URL | http://localhost:8005 | URL of Service A |
| SERVICE_C_URL | http://localhost:8007 | URL of Service C |

### Service C
| Variable | Default | Description |
|----------|---------|-------------|
| SERVICE_A_URL | http://localhost:8005 | URL of Service A |
| SERVICE_B_URL | http://localhost:8006 | URL of Service B |

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **httpx** - Async HTTP client
- **python-dotenv** - Environment variable management
