from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Health check"])


@router.get("/health")
async def health_check():
    return {"status": "ok"}
