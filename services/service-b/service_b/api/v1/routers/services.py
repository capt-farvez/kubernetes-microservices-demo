import httpx
from fastapi import APIRouter

from service_b.core.config import SERVICE_A_URL, SERVICE_C_URL

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/call-service-a")
async def call_service_a():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_A_URL}/api/v1/")
        return {
            "service": "B",
            "message": "Called Service A",
            "service_a_response": response.json()
        }


@router.get("/call-service-c")
async def call_service_c():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_C_URL}/api/v1/")
        return {
            "service": "B",
            "message": "Called Service C",
            "service_c_response": response.json()
        }
