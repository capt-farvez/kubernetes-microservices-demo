from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def read_root():
    return {"service": "C", "message": "Welcome to Service C"}


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "C"}
