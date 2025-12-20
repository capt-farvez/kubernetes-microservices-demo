import httpx
from fastapi import APIRouter

from service_a.core.config import SERVICE_B_URL, SERVICE_C_URL

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/call-service-b")
async def call_service_b():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_B_URL}/api/v1/")
        return {
            "service": "A",
            "message": "Called Service B",
            "service_b_response": response.json()
        }


@router.get("/call-service-c")
async def call_service_c():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_C_URL}/api/v1/")
        return {
            "service": "A",
            "message": "Called Service C",
            "service_c_response": response.json()
        }
