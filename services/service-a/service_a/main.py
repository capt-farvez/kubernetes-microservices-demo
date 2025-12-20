from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from service_a.api.v1.routers import health, services

app = FastAPI(
    title="Service A API",
    description="Service A API for microservices demo.",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url=None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(services.router, prefix="/api/v1")
