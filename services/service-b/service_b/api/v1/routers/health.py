from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def read_root():
    return {"service": "B", "message": "Welcome to Service B"}


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "B"}
