import httpx
from fastapi import APIRouter

from service_c.core.config import SERVICE_A_URL, SERVICE_B_URL

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/call-service-a")
async def call_service_a():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_A_URL}/api/v1/")
        return {
            "service": "C",
            "message": "Called Service A",
            "service_a_response": response.json()
        }


@router.get("/call-service-b")
async def call_service_b():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_B_URL}/api/v1/")
        return {
            "service": "C",
            "message": "Called Service B",
            "service_b_response": response.json()
        }
