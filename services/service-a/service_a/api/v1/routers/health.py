from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def read_root():
    return {"service": "A", "message": "Welcome to Service A"}


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "A"}
